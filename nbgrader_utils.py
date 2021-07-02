import os
import pandas as pd
passwd = ""
with open("pass",'r') as p:
        passwd = p.read()

def create_batch(filename):
    with open(filename, 'r') as f:
        
        os.popen("mkdir /home/keystone/Autograding/{}".format(f.name))
        
        students = pd.read_csv(filename, header=1)
        
        for std in students['email']:
            
            print(std)
            os.popen("mkdir /home/keystone/Autograding/{}/{}".format(f.name, std))
            
            
create_batch("AI-May21.csv")
            
            