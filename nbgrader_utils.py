import os
import pandas as pd
passwd = ""
with open("pass",'r') as p:
        passwd = p.read()

def create_batch(filename):
    with open(filename, 'r') as f:
        
        os.popen("mkdir /home/keystone/Autograding/{}".format(f.name))
        
        students = pd.read_csv(filename, header=0)
        
        for std in students.values:
            
            print(std)
            os.popen("mkdir /home/keystone/Autograding/{}/{}".format(f.name, std[1]))
            
            
create_batch("AI-May21.csv")
            
            