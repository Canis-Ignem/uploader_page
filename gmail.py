import pandas as pd
import numpy as np
import argparse
import smtplib
import os
import db


parser = argparse.ArgumentParser(description="NBGRADER partner script")
parser.add_argument('--assignment', metavar = 'a', type = str, required = True)
parser.add_argument('--batch', metavar = 'b', type = str, required = True)
args = vars(parser.parse_args())

sender_email = "jonperezetxebarria@gmail.com"

def send_emails(batch, assig):
    
    nb_dir = "home/keystone/Autograding/"
    
    for email in os.list(nb_dir+batch+"/submitted"):
        
            subject = "Grade "+assig
            #print(data.values[i][0])
            
            grade, max = db.get_grades(batch, email, assig)
            #print(receiver_email)
            #print(mess)
            body = "You scored: {}/{}".format(grade,max)
            pas= "mpmppwoxfvwnzbyg"
            '''
            with open("./pass",'r') as f:
                pas = f.readline()
            '''

            message = "Subject: {}\n\n{}".format(subject,body)
            print(message)
            
            
            try:
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.ehlo()
                s.starttls()
                s.login(sender_email, pas)
                s.sendmail(sender_email, email, message)         
                print( "Successfully sent email to: ", email)
                s.quit()
            except Exception as vx:
                
                print(vx)
            
            
def main():
    
    send_emails(args['batch'], args['assignment'])
    
if __name__ == '__main__':
    main()
