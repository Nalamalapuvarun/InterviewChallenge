import random
import sqlite3
from sqlite3 import Error
import string
import requests
import json

def generate_password(length, complexity):
    """Generate a random password with given length and complexity

    Complexity levels:
        Complexity == 1: return a password with only lowercase chars
        Complexity ==  2: Previous level plus at least 1 digit
        Complexity ==  3: Previous levels plus at least 1 uppercase char
        Complexity ==  4: Previous levels plus at least 1 punctuation char

    :param length: number of characters
    :param complexity: complexity level
    :returns: generated password
    """
    lower=string.ascii_lowercase
    upper=string.ascii_uppercase
    digits=string.digits
    punctuation=string.punctuation
    if complexity==1:
        password = ''.join(random.choice(lower) for _ in range(length))
    elif complexity==2:
        if length <2:
            return "password length should be minimum of 2 characters"
        else:
            password = ''.join(random.choices(digits, k=1))
            password = password + ''.join(random.choices(lower, k=1))
            password = password + ''.join(random.choice(lower+digits) for _ in range(length-2))
            l=list(password)
            random.shuffle(l)
            password = ''.join(l)
    elif complexity==3:
        if length <3:
            return "password length should be minimum of 3 characters"
        else:
            password = ''.join(random.choices(digits, k=1))
            password = password + ''.join(random.choices(lower, k=1))
            password = password + ''.join(random.choices(upper,k=1))
            password = password + ''.join(random.choice(lower+digits+upper) for _ in range(length-3))
            l=list(password)
            random.shuffle(l)
            password = ''.join(l)
    elif complexity==4:
        if length <4:
            return "password length should be minimum of 4 characters"
        else:
            password = ''.join(random.choices(digits, k=1))
            password = password + ''.join(random.choices(lower, k=1))
            password = password + ''.join(random.choices(upper,k=1))
            password = password + ''.join(random.choices(punctuation,k=1))
            password = password + ''.join(random.choice(lower+digits+upper+punctuation) for _ in range(length-4))
            l=list(password)
            random.shuffle(l)
            password = ''.join(l)
    return password

def check_password_level(password):
    """Return the password complexity level for a given password

    Complexity levels:
        Return complexity 1: If password has only lowercase chars
        Return complexity 2: Previous level condition and at least 1 digit
        Return complexity 3: Previous levels condition and at least 1 uppercase char
        Return complexity 4: Previous levels condition and at least 1 punctuation

    Complexity level exceptions (override previous results):
        Return complexity 2: password has length >= 8 chars and only lowercase chars
        Return complexity 3: password has length >= 8 chars and only lowercase and digits

    :param password: password
    :returns: complexity level
    """
    complexity=0
    lower=0
    upper=0
    digits=0
    punctuation=0
    for c in password:
        if c.islower():
            lower+=1
        elif c.isdigit():
            digits+=1
        elif c.isupper():
            upper+=1
        else:
            punctuation+=1

    if lower>0 and digits==0 and upper==0 and punctuation==0:
        complexity=1
    elif lower>0 and digits>0 and upper==0 and punctuation==0:
        complexity=2
    elif lower>0 and digits>0 and upper>0 and punctuation==0:
        complexity=3
    elif lower>0 and digits>0 and upper>0 and punctuation>0:
        complexity=4

    if len(password)>=8 and lower==len(password):
        complexity=2
    elif len(password)>= 8 and lower+digits==len(password):
        complexity=3
    return complexity

def check():
    value = False
    for _ in range(5):
        complexity_level = random.randint(1,4)
        pwd = generate_password(random.randint(6,12),complexity_level)
        result = check_password_level(pwd)
        if(complexity_level==result):
            value=True
    return value

def create_user(db_path):  # you may want to use: http://docs.python-requests.org/en/master/
    """Retrieve a random user from https://randomuser.me/api/
    and persist the user (full name and email) into the given SQLite db

    :param db_path: path of the SQLite db file (to do: sqlite3.connect(db_path))
    :return: None
    """
    request = requests.get("https://randomuser.me/api/")
    data=request.json()
    email= data['results'][0]['email']
    fname = data['results'][0]['name']['first']
    lname = data['results'][0]['name']['last']
    name = fname + ' ' + lname
    try:
        conn = sqlite3.connect(db_path)
        c=conn.cursor()
        create_table = """ CREATE TABLE IF NOT EXISTS user (
                                            name text,
                                            email CHAR(50),
                                            password CHAR(15)); """
        c.execute(create_table)
        insert_data = """ INSERT INTO user VALUES(?,?,?)"""
        param=(name,email,'null');
        c.execute(insert_data,param)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        conn.close()

def update_password(db_path):
    try:
        conn = sqlite3.connect(db_path)
        c=conn.cursor()
        retrieve_data=""" SELECT * from user;"""
        c.execute(retrieve_data)
        result=c.fetchmany(10)
        for i in range(10):
            username = result[i][0]
            pwd = generate_password(random.randint(6,12),random.randint(1,4))
            update_data = """UPDATE user SET password=? where name=? """
            param=(pwd,username);
            c.execute(update_data,param)
            conn.commit()
        conn.commit()
    except Error as e:
        print(e)
    finally:
        conn.close()

create_user("C:\\sqlite\db\oldb.db")
update_password("C:\\sqlite\db\oldb.db")
