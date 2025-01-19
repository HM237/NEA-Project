import sqlite3
import os
import smtplib
import  random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#User class which inserts into User Table
class User:
    def __init__(self, first_name, last_name, email, phone_number, date_of_birth):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.date_of_birth= date_of_birth
    
    def add_User(self):
        with sqlite3.connect('test2.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO  User (FirstName, LastName, Email, PhoneNumber, DoB) VALUES (?,?,?,?,?)', (self.first_name,self.last_name,self.email,self.phone_number, self.date_of_birth))
            conn.commit()

#Nikah class which inserts into Nikah Table
class Nikah:
    def __init__(self, user_id,groom_first_name, groom_last_name, bride_first_name, bride_last_name, time, date, post_code, address_line):
        self.user_id = user_id
        self.groom_first_name = groom_first_name
        self.groom_last_name = groom_last_name        
        self.bride_first_name = bride_first_name
        self.bride_last_name = bride_last_name
        self.time = time
        self.date = date
        self.post_code = post_code
        self.address_line = address_line

    def add_Nikah(self):
        with sqlite3.connect('test2.db') as conn:
             cursor = conn.cursor()
             cursor.execute('INSERT INTO  Nikah (UserID,GroomFirstName,GroomLastName,BrideFirstName,BrideLastName,Time, Date, PostCode,AddressLine) VALUES (?,?,?,?,?,?,?,?,?)', (self.user_id, self.groom_first_name,self.groom_last_name, self.bride_first_name, self.bride_last_name, self.time, self.date, self.post_code, self.address_line))

             conn.commit()  

#Madrasah class which inserts into Madrasah Table
class Madrasah:
    def __init__(self, user_id, time, date, child_fname, child_lname, child_date_of_birth ):
        self.user_id = user_id
        self.time = time
        self.date = date
        self.child_fname = child_fname
        self.child_lname = child_lname
        self.child_date_of_birth = child_date_of_birth

    def add_Madrasah(self):
        with sqlite3.connect('test2.db') as conn:
             cursor = conn.cursor()
             cursor.execute('INSERT INTO  Madrasah (UserID,Time, Date, ChildFirstName,ChildLastName ,ChildDoB) VALUES (?,?,?,?,?,?)', (self.user_id,self.time,self.date,self.child_fname,self.child_lname,self.child_date_of_birth ))

#Payment class which inserts into Payment Table
class Payment:
    def __init__(self, user_id,post_code, address_line,payment_method, CVC, price):
        self.user_id = user_id
        self.post_code = post_code
        self.address_line = address_line
        self.payment_method = payment_method
        self.CVC = CVC
        self.price = price


    def add_Payment(self):
        with sqlite3.connect('test2.db') as conn:
             cursor = conn.cursor()
             cursor.execute('INSERT INTO  Payment (UserID,PaymentMethod,AddressLine,PostCode,CVC, Price) VALUES (?,?,?,?,?,?)', (self.user_id, self.payment_method, self.address_line, self.post_code, self.CVC, self.price))
             conn.commit()


#Clashed class which checks for unavailable bookings
class Clashed:
    def __init__(self,time, date):
        self.time = time
        self.date = date
    
    @classmethod
    def clashed(cls, time, date):
        exists = False
        with sqlite3.connect('test2.db') as conn:
            cursor = conn.cursor()
            tables = ['Nikah', 'Madrasah', 'Service']
            for table in tables:
                cursor.execute(f'SELECT * FROM User u JOIN {table} t ON u.UserID = t.UserID WHERE time = "{time}" AND date = "{date}"')
                try:
                    result = cursor.fetchone()[0] > 0
                    if result:
                        exists = True
                        break
                except Exception as e:
                    errors = e
        return exists

#Verification class which will execute the verification processs
class Verification:
    def __init__(self, email, number):
        self.email = email
        self.number = number
    
    def send_verification_email(self):
        #using os so that personal details aren't shown
        sender_email = os.environ.get('MY_EMAIL')
        password = os.environ.get('MY_PASSWORD')
        receiver_email = f'{self.email}'
        code = self.number
    
        if sender_email:
            print(f'Successfully retrieved sender email')

        # Create the message object
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "Verification Code"
        
        #email
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Email Example</title>
        </head>
        <body>
            <h1 style="font-size: 30px;">Masjid Al-Ansar Verification Code!</h1>
            <p style="font-size: 18px;">Hello,<br>
            Please use the verification code below for your booking at Masjid Al-Ansar. The code will be valid for 2 minutes.</p>
            
            <p style="font-size: 20px; font-weight: bold;">Verification Code: {code}</p>
            
            
            <p style="font-size: 16px; color: red;">If you didn't generate this code, someone else might be trying to use you email account.</p>
            <p style="font-size: 18px;">Thanks,<br> Masjid Al-Ansar Team </p>
            <p> <a title="Masjid Al-Ansar" href="http://127.0.0.1:5000/about-us">Masjid Al-Ansar</a> </p>
        </body>
        </html>
        """

        # Attaching the HTML content to the message
        msg.attach(MIMEText(html_content, 'html'))

        # Connecting to the Gmail SMTP server and sending the email
        try:
            # Establishing a secure session with Gmail's SMTP server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()  
            server.login(sender_email, password)  

            # Sending the email
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email sent successfully!")

        except Exception as e:
            error = "Error: {e}"
        finally:
            server.quit()
        return code ##we should probably change this line idk

class Summary:
    def __init__(self, email):
        self.email = email
    
    def send_summary_email(self):
        #using os so that personal details aren't shown
        sender_email = os.environ.get('MY_EMAIL')
        password = os.environ.get('MY_PASSWORD')
        receiver_email = f'{self.email}'
    
        if sender_email:
            print(f'Successfully retrieved sender email')

        # Create the message object
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "Summary Link"
        
        #email
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title> Summary Email </title>
        </head>
        <body>
            <h1 style="font-size: 30px;">Masjid Al-Ansar Summary Email!</h1>
            <p style="font-size: 18px;">Hello,<br>
            Please use the below link to find a summary of your booking at Masjid Al-Ansar</p>
            
            <p style="font-size: 20px; font-weight: bold;">Summary: LINK</p>
            
            
            <p style="font-size: 16px; color: red;">If you didn't generate this link, someone else might be trying to use you email account.</p>
            <p style="font-size: 18px;">Thanks,<br> Masjid Al-Ansar Team </p>
            <p> <a title="Masjid Al-Ansar" href="http://127.0.0.1:5000/about-us">Masjid Al-Ansar</a> </p>
        </body>
        </html>
        """

        # Attaching the HTML content to the message
        msg.attach(MIMEText(html_content, 'html'))

        # Connecting to the Gmail SMTP server and sending the email
        try:
            # Establishing a secure session with Gmail's SMTP server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()  
            server.login(sender_email, password)  

            # Sending the email
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email sent successfully!")

        except Exception as e:
            error = f"Error: {e}"
        finally:
            server.quit()
        return f'Success?'