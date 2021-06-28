import pymysql
from sqlalchemy import create_engine
from md5 import md5


engine = create_engine("mysql+pymysql://phpmyadmin:Estocolmo597B@localhost:3306/phpmyadmin")
conn = engine.connect()
#conn.execute("CREATE TABLE users(user varchar(32) PRIMARY KEY, md5 text )")
#conn.cursor().execute("INSERT INTO users VALUES('keystone','6458f3bfa6486a2be61b9fb6f37645c8')")

def get_sum(user):
    
    res = conn.execute("SELECT md5 from users where user = '{}'".format(user))
    return res.fetchone()[0]

def add_user(user, pas, email, DoB, country_of_residence, batch, gender ):
    try:
        
        md5_sum = md5(pas)
        conn.execute("INSERT INTO users VALUES('{}','{}','{}','{}','{}','{}','{}')".format(user, md5_sum, batch, email, gender, country_of_residence, DoB))
        return True
    except:
        return False

def add_user_grades(user):
    try:

        conn.execute("INSERT INTO grades VALUES('{}')".format(user))
        return True
    except:
        return False