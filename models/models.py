import sqlite3
import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#User class which deals with  User Table
class User:
    def __init__(self, first_name, last_name, email, phone_number, date_of_birth):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.date_of_birth= date_of_birth
    
    def add_User(self):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO  User (FirstName, LastName, Email, PhoneNumber, DoB) VALUES (?,?,?,?,?)', (self.first_name,self.last_name,self.email,self.phone_number, self.date_of_birth))
            conn.commit()

    def update(self,userid):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            query = '''
            UPDATE User
            SET FirstName = ?, LastName = ?, Email = ?, PhoneNumber = ?, DoB = ?
            WHERE UserID = ?
            '''
            parameters = (self.first_name,self.last_name,self.email,self.phone_number, self.date_of_birth, userid)
            cursor.execute(query, parameters)
            conn.commit()              

#Nikah class which deals with Nikah Table
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

    #this adds the data to the Nikah Table
    def add_Nikah(self):
        with sqlite3.connect('database.db') as conn:
             cursor = conn.cursor()
             cursor.execute('INSERT INTO  Nikah (UserID,GroomFirstName,GroomLastName,BrideFirstName,BrideLastName,Time, Date, PostCode,AddressLine) VALUES (?,?,?,?,?,?,?,?,?)', (self.user_id, self.groom_first_name,self.groom_last_name, self.bride_first_name, self.bride_last_name, self.time, self.date, self.post_code, self.address_line))
             conn.commit()  

    #this updates  a specific row in the Nikah Table
    def update(self):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            query = '''
            UPDATE Nikah
            SET GroomFirstName = ?, GroomLastName = ?, BrideFirstName = ?, BrideLastName = ?, Time = ?, Date = ?, PostCode = ?, AddressLine = ?
            WHERE UserID = ?
            '''
            parameters = (self.groom_first_name, self.groom_last_name, self.bride_first_name, self.bride_last_name, self.time, self.date, self.post_code, self.address_line, self.user_id)
            cursor.execute(query, parameters)
            conn.commit()

    def delete(userid):
        success = False
        try:    
            with sqlite3.connect('database.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"DELETE FROM User WHERE UserID = {userid}")
                    cursor.execute(f"DELETE FROM Nikah WHERE UserID = {userid}")
                    cursor.execute(f"DELETE FROM Hash WHERE UserID = {userid}")
                    conn.commit()
                    conn.close()
                    success = True 
            return success
        except:
            error = 'Error'       
            return success

#Madrasah class which deals with Madrasah Table
class Madrasah:
    def __init__(self, user_id, time, date, child_fname, child_lname, child_date_of_birth ):
        self.user_id = user_id
        self.time = time
        self.date = date
        self.child_fname = child_fname
        self.child_lname = child_lname
        self.child_date_of_birth = child_date_of_birth

    def add_Madrasah(self):
        with sqlite3.connect('database.db') as conn:
             cursor = conn.cursor()
             cursor.execute('INSERT INTO  Madrasah (UserID,Time, Date, ChildFirstName,ChildLastName ,ChildDoB) VALUES (?,?,?,?,?,?)', (self.user_id,self.time,self.date,self.child_fname,self.child_lname,self.child_date_of_birth ))

    def update(self):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            query = '''
            UPDATE Madrasah
            SET ChildFirstName = ?, ChildLastName = ?, ChildDoB = ?, BrideLastName = ?, Time = ?, Date = ?, PostCode = ?, AddressLine = ?
            WHERE UserID = ?
            '''
            parameters = (self.time,self.date,self.child_fname,self.child_lname,self.child_date_of_birth, self.user_id)
            cursor.execute(query, parameters)
            conn.commit()             

#Tours class which deals with Tours Table
class Tours:
    def __init__(self, user_id, time, date, number_of_people):
        self.user_id = user_id
        self.time = time
        self.date = date
        self.number_of_people= number_of_people

    def add_Tour(self):
        with sqlite3.connect('database.db') as conn:
             cursor = conn.cursor()
             cursor.execute('INSERT INTO  Tours (UserID,Time, Date, NumberOfPeople) VALUES (?,?,?,?)', (self.user_id,self.time,self.date,self.number_of_people))

    def update(self):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            query = '''
            UPDATE Tours
            SET Time = ?, Date= ?, NumberOfPeople= ?
            WHERE UserID = ?
            '''
            parameters = (self.time,self.date,self.number_of_people, self.user_id)
            cursor.execute(query, parameters)
            conn.commit()             

#Functions class which deals with Tours Table
class Funtions:
    def __init__(self, user_id, time, date, post_code, address_line):
        self.user_id = user_id
        self.time = time
        self.date = date
        self.post_code = post_code
        self.address_line = address_line

    def add_Function(self):
        with sqlite3.connect('database.db') as conn:
             cursor = conn.cursor()
             cursor.execute('INSERT INTO  Functions (UserID,Time, Date, PostCode, AddressLine) VALUES (?,?,?,?.?)', (self.user_id,self.time,self.date,self.post_code, self.address_line))    

    def update(self):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            query = '''
            UPDATE Functions
            SET Time = ?, Date= ?, PostCode = ?, AddressLine - ?
            WHERE UserID = ?
            '''
            parameters = (self.time,self.date,self.post_code, self.address_line, self.user_id)
            cursor.execute(query, parameters)
            conn.commit()                     

#Payment class which inserts into Payment Table
class Payment:
    def __init__(self, user_id,post_code, address_line,payment_method, price):
        self.user_id = user_id
        self.post_code = post_code
        self.address_line = address_line
        self.payment_method = payment_method
        self.price = price


    def add_Payment(self):
        with sqlite3.connect('database.db') as conn:
             cursor = conn.cursor()
             cursor.execute('INSERT INTO  Payment (UserID,PaymentMethod,AddressLine,PostCode,Price) VALUES (?,?,?,?,?)', (self.user_id, self.payment_method, self.address_line, self.post_code, self.price))
             conn.commit()

#Clashed class which checks for unavailable bookings
class Clashed:
    def __init__(self,time, date):
        self.time = time
        self.date = date
    
    @classmethod
    def clashed(cls, time, date):
        exists = False #assumes that the time and date has not already been booked
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            tables = ['Nikah', 'Madrasah', 'Function']
            for table in tables:
                cursor.execute(f'SELECT * FROM User u JOIN {table} t ON u.UserID = t.UserID WHERE time = "{time}" AND date = "{date}"')
                try:
                    result = cursor.fetchone()[0] > 0
                    if result:
                        exists = True #if it does exist we return True
                        break
                except Exception as e:
                    errors = e
        return exists

#Hash class which performs the hash algorithm
class Hash:    
    def __init__(self, time,date, userid):
        self.time = time 
        self.date = date
        self.userid = userid


    def hash_algorithm(self):
        #joining the time,date and userid to make the hash value. Imporant to use the id to make the digest more specific
        string = f'{self.date}{self.time}{self.userid}'
        string = re.sub(r'[-:]', '', string)
        arr = [0] * 20 #creating a 160 bit array
        digest = ''
        for index, character in enumerate(string):
            ascii_value = ord(character)
            for i in range (20):
                value = ((arr[i] + ascii_value * (index + 1) + i ) * 17) % 256  #multiplying by 17 makes the pattern more random
                arr[i] = value
        for byte in arr:
            digest += format(byte, '02x') #converting it into hexadecimal
        return digest

    def add_digest(self, digest):
        #storing the digest in the Hash Table along with UserID,Time and Date
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO  Hash (UserID,Digest,Time,Date) VALUES (?,?,?,?)', (self.userid, digest, self.time, self.date))
            conn.commit()
        return digest

#Email class which will execute the verification/summary processs
class Email:
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

        # Creating the message object
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "Verification Code"
        
        #email content itself
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

        # Attaching the content to the email itself
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
    
    def send_summary_email(self, service):
        #using os so that personal details aren't shown
        sender_email = os.environ.get('MY_EMAIL')
        password = os.environ.get('MY_PASSWORD')
        receiver_email = f'{self.email}'
        link  = self.number

        if sender_email:
            print(f'Successfully retrieved sender email')

        # Creating the message object
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "Summary Link"
        
        #the email itself
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
            Please click the below link to find a summary of your booking at Masjid Al-Ansar</p>
            
            <p style="font-size: 20px; font-weight: bold;">Summary Link: <a href="http://127.0.0.1:5000/booking/{service}/{link}">Click This</a> </p>
            
            
            <p style="font-size: 16px; color: red;">If you didn't generate this link, someone else might be trying to use you email account.</p>
            <p style="font-size: 18px;">Thanks,<br> Masjid Al-Ansar Team </p>
            <p> <a title="Masjid Al-Ansar" href="http://127.0.0.1:5000/about-us">Masjid Al-Ansar</a> </p>
        </body>
        </html>
        """

        # Attaching the content to the email itself
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
