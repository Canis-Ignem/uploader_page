import os
import pandas as pd
passwd = ""
with open("pass",'r') as p:
        passwd = p.read()

def create_batch(filename):
    with open(filename, 'r') as f:
        
        os.popen("mkdir /home/keystone/Autograding/{}".format(f.name)).write(passwd)
        
        students = pd.read_csv(filename)
        
        for std in students:
            
            os.popen("mkdir /home/keystone/Autograding/{}/{}".format(f.name, std['email'])).write(passwd)
            
            
create_batch("AI-May21.csv")
            
            