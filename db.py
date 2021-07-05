from sqlalchemy import create_engine
import sqlite3 as sql
from md5 import md5
import pandas as pd
import pymysql


passwd = ""
with open("passdb",'r') as p:
        passwd = p.read()
        
engine = create_engine("mysql+pymysql://phpmyadmin:{}@localhost:3306/phpmyadmin".format(passwd[:-1]))
conn = engine.connect()


def get_sum(user):
    
    res = conn.execute("SELECT md5 from users where user = '{}'".format(user))
    return res.fetchone()[0]

def add_user(user, pas, email, DoB, country_of_residence, batch, gender ):
    try:
        
        md5_sum = md5(pas)
        conn.execute("INSERT INTO users (user, md5, batch, email, gender, country_of_residence, DoB) VALUES('{}','{}','{}','{}','{}','{}','{}')".format(user, md5_sum, batch, email, gender, country_of_residence, DoB))
        return True
    except:
        return False

def add_user_grades(user):
    try:

        conn.execute("INSERT INTO grades VALUES('{}',0,0)".format(user))
        return True
    except:
        return False

def get_batch(user):
    
    res = conn.execute("SELECT batch from users where user = '{}'".format(user))
    
    batch = res.fetchone()
    return str(batch[0])

def get_email(user):
    
    res = conn.execute("SELECT email from users where user = '{}'".format(user))
    
    email = res.fetchone()
    return str(email[0])


def get_grades(batch,email,ex):
    
    try:
        con = sql.connect("/home/keystone/Autograding/{}/gradebook.db".format(batch))
        
        q1 = "SELECT id FROM assignment where name ='{}'".format(ex)
        ass_id = pd.read_sql_query( q1 , con).values[0][0]
        
        q2 = "Select id from submitted_assignment where student_id = '{}' and assignment_id = '{}' ".format(email,ass_id)  
        nb_id = pd.read_sql_query( q2 , con).values[0][0]
        
        q3 = "Select id from submitted_notebook where assignment_id = '{}'".format(nb_id)
        nb_id = pd.read_sql_query( q3 , con).values[0][0]

        q4 = "Select auto_score,cell_id from grade where notebook_id = '{}'".format(nb_id)
        grades = pd.read_sql_query( q4 , con)
        
        cell_list = grades['cell_id'].values.tolist()
        as_str = ','.join("\'"+str(cell_list[i])+ "\'"  for i in range(len(cell_list)))
        q5 = "Select max_score from grade_cells where id IN ({})".format( as_str )
        max_score = pd.read_sql_query( q5 , con)
        #print(max_score['max_score'].sum())
       
        #report = " The student:  {} \n Assigment:   {} \n Total marks: {}/{}".format(email,ex,grades['auto_score'].sum(),max_score['max_score'].sum())
        #print(report)
        con.close()
        return grades['auto_score'].sum(), max_score['max_score'].sum()
    except:
        #print("No submission for that student")
        return 0, 1
