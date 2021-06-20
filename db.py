import pymysql
from sqlalchemy import create_engine
from md5 import md5


engine = create_engine("mysql+pymysql://phpmyadmin:Estocolmo597B@localhost/phpmyadmin?host=localhost?port=3306")
conn = engine.connect()
#conn.cursor().execute("CREATE TABLE users(user text, md5 text PRIMARY KEY)")
#conn.cursor().execute("INSERT INTO users VALUES('keystone','6458f3bfa6486a2be61b9fb6f37645c8')")

def get_sum(user):
    
    res = conn.cursor().execute("SELECT md5 from users where user = '{}'".format(user))
    return res.fetchone()[0]

def add_user(user, pas):
    try:
        
        md5_sum = md5(pas)
        conn.cursor().execute("INSERT INTO users VALUES('{}','{}')".format(user, md5_sum))
        conn.commit()
        return True
    except:
        return False
    
print(get_sum("keystone"))
