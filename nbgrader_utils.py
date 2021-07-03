import os
import pandas as pd
passwd = ""
with open("pass",'r') as p:
        passwd = p.read()

def create_batch(filename):
    with open(filename, 'r') as f:
        
        os.popen("mkdir /home/keystone/Autograding/{}/submitted".format(f.name[:-4]))
        
        students = pd.read_csv(filename, header=0)
        
        for std in students.values:
            
            print(std)
            os.popen("mkdir /home/keystone/Autograding/{}/submitted/{}".format(f.name[:-4], std[1]))
            
            
def create_ex(exercise, batch):
    
    for fldr in os.listdir("/home/keystone/Autograding/{}/submitted".format(batch)):
        
        os.popen("mkdir /home/keystone/Autograding/{}/submitted/{}/{}".format(batch,fldr,exercise))

create_batch("AI-May21.csv")
create_ex("ml1", "AI-May21")