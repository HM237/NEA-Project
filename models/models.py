import sqlite3
import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

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
    def __init__(self, user_id,groom_first_name, groom_last_name, bride_first_name, bride_last_name, post_code, address_line):
        self.user_id = user_id
        self.groom_first_name = groom_first_name
        self.groom_last_name = groom_last_name        
        self.bride_first_name = bride_first_name
        self.bride_last_name = bride_last_name
        self.post_code = post_code
        self.address_line = address_line

    #this adds the data to the Nikah Table
    def add_Nikah(self):
        with sqlite3.connect('database.db') as conn:
             cursor = conn.cursor()
             cursor.execute('INSERT INTO  Nikah (UserID,GroomFirstName,GroomLastName,BrideFirstName,BrideLastName,PostCode,AddressLine) VALUES (?,?,?,?,?,?,?)', (self.user_id, self.groom_first_name,self.groom_last_name, self.bride_first_name, self.bride_last_name,self.post_code, self.address_line))
             conn.commit()  

    #this updates  a specific row in the Nikah Table
    def update(self):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            query = '''
            UPDATE Nikah
            SET GroomFirstName = ?, GroomLastName = ?, BrideFirstName = ?, BrideLastName = ?,PostCode = ?, AddressLine = ?
            WHERE UserID = ?
            '''
            parameters = (self.groom_first_name, self.groom_last_name, self.bride_first_name, self.bride_last_name,self.post_code, self.address_line, self.user_id)
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
                    cursor.execute(f"DELETE FROM Payment WHERE UserID = {userid}")                    
                    conn.commit()
                    conn.close()
                    success = True 
            return success
        except:
            error = 'Error'       
            return success

#Madrasah class which deals with Madrasah Table
class Madrasah:
    def __init__(self, user_id,child_fname, child_lname, child_date_of_birth ):
        self.user_id = user_id
        self.child_fname = child_fname
        self.child_lname = child_lname
        self.child_date_of_birth = child_date_of_birth

    def add_Madrasah(self):
        with sqlite3.connect('database.db') as conn:
             cursor = conn.cursor()
             cursor.execute('INSERT INTO  Madrasah (UserID,ChildFirstName,ChildLastName ,ChildDoB) VALUES (?,?,?,?)', (self.user_id,self.child_fname,self.child_lname,self.child_date_of_birth ))

    def update(self):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            query = '''
            UPDATE Madrasah
            SET ChildFirstName = ?, ChildLastName = ?, ChildDoB = ?
            WHERE UserID = ?
            '''
            parameters = (self.child_fname,self.child_lname,self.child_date_of_birth,self.user_id)
            cursor.execute(query, parameters)
            conn.commit()

    def delete(userid):
        success = False
        try:    
            with sqlite3.connect('database.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"DELETE FROM User WHERE UserID = {userid}")
                    cursor.execute(f"DELETE FROM Madrasah WHERE UserID = {userid}")
                    cursor.execute(f"DELETE FROM Hash WHERE UserID = {userid}")
                    conn.commit()
                    conn.close()
                    success = True 
            return success
        except:
            error = 'Error'       
            return success                   

#Tours class which deals with Tours Table
class Tours:
    def __init__(self, user_id, number_of_people):
        self.user_id = user_id
        self.number_of_people= number_of_people

    def add_Tour(self):
        with sqlite3.connect('database.db') as conn:
             cursor = conn.cursor()
             cursor.execute('INSERT INTO  Tours (UserID,NumberOfPeople) VALUES (?,?)', (self.user_id,self.number_of_people))

    def update(self):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            query = '''
            UPDATE Tours
            SET NumberOfPeople= ?
            WHERE UserID = ?
            '''
            parameters = (self.number_of_people, self.user_id)
            cursor.execute(query, parameters)
            conn.commit()       

    def delete(userid):
        success = False
        try:    
            with sqlite3.connect('database.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"DELETE FROM User WHERE UserID = {userid}")
                    cursor.execute(f"DELETE FROM Tours WHERE UserID = {userid}")
                    cursor.execute(f"DELETE FROM Hash WHERE UserID = {userid}")
                    cursor.execute(f"DELETE FROM Payment WHERE UserID = {userid}")                                        
                    conn.commit()
                    conn.close()
                    success = True 
            return success
        except:
            error = 'Error'       
            return success                 

#Functions class which deals with Functions Table
class Functions:
    def __init__(self, user_id,post_code, address_line):
        self.user_id = user_id
        self.post_code = post_code
        self.address_line = address_line

    def add_Function(self):
        with sqlite3.connect('database.db') as conn:
             cursor = conn.cursor()
             cursor.execute('INSERT INTO  Function (UserID,PostCode, AddressLine) VALUES (?,?,?)', (self.user_id,self.post_code, self.address_line))    

    def update(self):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            query = '''
            UPDATE Function
            SET PostCode = ?, AddressLine = ?
            WHERE UserID = ?
            '''
            parameters = (self.post_code, self.address_line,self.user_id)
            cursor.execute(query, parameters)
            conn.commit()                     

    def delete(userid):
        success = False
        try:    
            with sqlite3.connect('database.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"DELETE FROM User WHERE UserID = {userid}")
                    cursor.execute(f"DELETE FROM Function WHERE UserID = {userid}")
                    cursor.execute(f"DELETE FROM Hash WHERE UserID = {userid}")
                    conn.commit()
                    conn.close()
                    success = True 
            return success
        except:
            error = 'Error'       
            return success
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
        try:
            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute(f'SELECT * FROM User u JOIN Hash t ON u.UserID = t.UserID WHERE time = "{time}" AND date = "{date}"')
                result = cursor.fetchone()
                if result is not None:
                    return True
                else:
                    return False
        except:
            return True

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
    
    def update(self,newdigest):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            query = '''
            UPDATE Hash
            SET Digest = ?, Time = ?, Date = ?
            WHERE UserID = ? 
            '''
            parameters = (newdigest, self.time, self.date, self.userid)
            cursor.execute(query, parameters)
            conn.commit()        

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


class Validation:
    @classmethod
    def validate(cls, data):
        errors = []
        for key, value in data.items():
            if key =='Time':
                    # Parse booking time

                bookingtime = datetime.strptime(value, '%H:%M')

                # Define allowed time range
                start_time = datetime.strptime('16:30', '%H:%M')
                end_time = datetime.strptime('21:00', '%H:%M')

                # Check if booking time is within range
                if not (start_time <= bookingtime <= end_time):
                    errors.append(f"Booking time must be between 16:30 and 20:00.")
                # Check if booking time is at 15-minute intervals
                if bookingtime.minute % 15 != 0:
                    errors.append(f"Booking time must be at 15-minute intervals (e.g., 16:45, 17:00).")

            elif key == 'Date':
                bookingdate = datetime.strptime(value, '%Y-%m-%d') 

                start_date = datetime.strptime('2025-01-01', '%Y-%m-%d')
                end_date = datetime.strptime('2030-12-31', '%Y-%m-%d')

                if not (start_date <= bookingdate <= end_date):
                    errors.append(f"Booking date must be between 01/01/2025 and 31/12/2030.")

            elif key == 'Number Of People':
                if not value.isnumeric():
                    errors.append('Value has to be a number')

            elif key == 'Child Date of Birth':
                match = re.match(r"""^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$""", value)
                if not match:
                    errors.append(f'{key} must be filled in.')
                else:
                    childdob = datetime.strptime(value, '%Y-%m-%d') 

                    start_date = datetime.strptime('2000-01-01', '%Y-%m-%d')
                    end_date = datetime.strptime('2020-12-31', '%Y-%m-%d')

                    if not (start_date <= childdob <= end_date):
                        errors.append(f"Child is too old to attend this madrasash.")

            elif key == 'Email':
                match = re.match(r"""^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$""", value)
                if not match:
                    errors.append(f"{key} must be a valid email")


            elif key == 'Post Code' or key == 'Address Line':
                match = re.match(r"""(\w+\s\w+)""", value)
                if not match:
                    errors.append(f"{key} must be a valid post code.")

            else:
                match = re.match(r"""^(?![\s.]+$)[a-zA-Z\s.]+$""", value)
                if not match:
                    errors.append(f"{key} must be alphabetical characters.")
                    
        if errors:
            errors = '\n'.join(errors)
            return errors 
