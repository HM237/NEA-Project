import sqlite3
import os
import re
import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

class DatabaseError(Exception):
    pass

class ServerError(Exception):
    pass

class UnboundLocalErrors(Exception):
    pass

class SocketError(Exception):
    pass

#User class which deals with  User Table
class User:
    def __init__(self, first_name, last_name, email, phone_number, date_of_birth):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.date_of_birth= date_of_birth
    
    def add_User(self):
        try:
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                cursor.execute('INSERT INTO  User (FirstName, LastName, Email, PhoneNumber, DoB) VALUES (?,?,?,?,?)', (self.first_name,self.last_name,self.email,self.phone_number, self.date_of_birth))
                connection.commit()
        
        except sqlite3.OperationalError as e:
            print(f'{e} in normal user')            
            raise DatabaseError("There was an operational error.")


        except sqlite3.DatabaseError as e:
            raise DatabaseError(f"Database error: {e}")

        finally:
            cursor.close()
            connection.close()

    def update(self,userid):
        try:
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                query = '''
                UPDATE User
                SET FirstName = ?, LastName = ?, Email = ?, PhoneNumber = ?, DoB = ?
                WHERE UserID = ?
                '''
                parameters = (self.first_name,self.last_name,self.email,self.phone_number, self.date_of_birth, userid)
                cursor.execute(query, parameters)
                connection.commit()

        except sqlite3.OperationalError as e:
            print(f'{e} in user')                        
            raise DatabaseError("There was an operational error.")

        except sqlite3.DatabaseError as e:
            raise DatabaseError(f"Database error: {e}")

        finally:
            cursor.close()
            connection.close()            

#Nikah class which deals with Nikah Table
class Nikah:
    def __init__(self, user_id,groom_first_name, groom_last_name, bride_first_name, bride_last_name):
        self.user_id = user_id
        self.groom_first_name = groom_first_name
        self.groom_last_name = groom_last_name        
        self.bride_first_name = bride_first_name
        self.bride_last_name = bride_last_name

    #this adds the data to the Nikah Table
    def add_Nikah(self):
        try:
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                cursor.execute('INSERT INTO  Nikah (UserID,GroomFirstName,GroomLastName,BrideFirstName,BrideLastName) VALUES (?,?,?,?,?)', (self.user_id, self.groom_first_name,self.groom_last_name, self.bride_first_name, self.bride_last_name))
                connection.commit()  

        except sqlite3.OperationalError as e:
            print(f'{e} in nikah')            
            raise DatabaseError("There was an operational error.")

        except sqlite3.DatabaseError as e:
            raise DatabaseError(f"Database error: {e}")

        finally:
            cursor.close()
            connection.close()                      

    #this updates  a specific row in the Nikah Table
    def update(self):
        try:
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                query = '''
                UPDATE Nikah
                SET GroomFirstName = ?, GroomLastName = ?, BrideFirstName = ?, BrideLastName = ?
                WHERE UserID = ?
                '''
                parameters = (self.groom_first_name, self.groom_last_name, self.bride_first_name, self.bride_last_name,self.user_id)
                cursor.execute(query, parameters)            
                connection.commit()

        except sqlite3.OperationalError as e:
            print(f'{e} in updatenikah')            
            raise DatabaseError("There was an operational error.")

        except sqlite3.DatabaseError as e:
            raise DatabaseError(f"Database error: {e}")

        finally:
            cursor.close()
            connection.close()                      

    def delete(userid):
        success = False
        try:    
            with sqlite3.connect('database.db') as connection:
                    cursor = connection.cursor()
                    cursor.execute(f"DELETE FROM User WHERE UserID = {userid}")
                    cursor.execute(f"DELETE FROM Nikah WHERE UserID = {userid}")
                    cursor.execute(f"DELETE FROM Hash WHERE UserID = {userid}")
                    cursor.execute(f"DELETE FROM Payment WHERE UserID = {userid}")                    
                    success = True 
            return success
        
        except sqlite3.OperationalError as e:
            raise DatabaseError("There was an operational error.")

        except sqlite3.DatabaseError as e:
            raise DatabaseError(f"Database error: {e}")

        finally:
            cursor.close()
            connection.close()      

#Madrasah class which deals with Madrasah Table
class Madrasah:
    def __init__(self, user_id,child_fname, child_lname, child_date_of_birth ):
        self.user_id = user_id
        self.child_fname = child_fname
        self.child_lname = child_lname
        self.child_date_of_birth = child_date_of_birth

    def add_Madrasah(self):
        try:
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                cursor.execute('INSERT INTO  Madrasah (UserID,ChildFirstName,ChildLastName ,ChildDoB) VALUES (?,?,?,?)', (self.user_id,self.child_fname,self.child_lname,self.child_date_of_birth ))

        except sqlite3.OperationalError as e:
            raise DatabaseError("There was an operational error.")

        except sqlite3.DatabaseError as e:
            raise DatabaseError(f"Database error: {e}")

        finally:
            cursor.close()
            connection.close()                      

    def update(self):
        try:
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                query = '''
                UPDATE Madrasah
                SET ChildFirstName = ?, ChildLastName = ?, ChildDoB = ?
                WHERE UserID = ?
                '''
                parameters = (self.child_fname,self.child_lname,self.child_date_of_birth,self.user_id)
                cursor.execute(query, parameters)
                connection.commit()

        except sqlite3.OperationalError as e:
            raise DatabaseError("There was an operational error.")

        except sqlite3.DatabaseError as e:
            raise DatabaseError(f"Database error: {e}")

        finally:
            cursor.close()
            connection.close()                      

    def delete(userid):
        success = False
        try:    
            with sqlite3.connect('database.db') as connection:
                    cursor = connection.cursor()
                    cursor.execute(f"DELETE FROM User WHERE UserID = {userid}")
                    cursor.execute(f"DELETE FROM Madrasah WHERE UserID = {userid}")
                    cursor.execute(f"DELETE FROM Hash WHERE UserID = {userid}")
                    success = True 
            return success
        
        except sqlite3.OperationalError as e:
            raise DatabaseError("There was an operational error.")

        except sqlite3.DatabaseError as e:
            raise DatabaseError(f"Database error: {e}")

        finally:
            cursor.close()
            connection.close()                      

#Tours class which deals with Tours Table
class Tours:
    def __init__(self, user_id, number_of_people, eventid):
        self.user_id = user_id
        self.number_of_people= number_of_people
        self.eventid = eventid

    def add_Tour(self):
        try:
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                cursor.execute('INSERT INTO  Tour (UserID,NumberOfPeople, EventTypeID) VALUES (?,?,?)', (self.user_id,self.number_of_people, self.eventid))

        except sqlite3.OperationalError as e:
            raise DatabaseError("There was an operational error.")
        
        except sqlite3.DatabaseError as e:
            raise DatabaseError(f"Database error: {e}")

        finally:
            cursor.close()
            connection.close()                      

    def update(self):
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            query = '''
            UPDATE Tour
            SET NumberOfPeople= ?, EventTypeID = ?
            WHERE UserID = ?
            '''
            parameters = (self.number_of_people,self.eventid, self.user_id)
            cursor.execute(query, parameters)
            connection.commit()       

    def delete(userid):
        success = False
        try:    
            with sqlite3.connect('database.db') as connection:
                    cursor = connection.cursor()
                    cursor.execute(f"DELETE FROM User WHERE UserID = {userid}")
                    cursor.execute(f"DELETE FROM Tour WHERE UserID = {userid}")
                    cursor.execute(f"DELETE FROM Hash WHERE UserID = {userid}")
                    connection.commit()
                    success = True 
            return success
        
        except sqlite3.OperationalError as e:
            raise DatabaseError("There was an operational error.")

        except sqlite3.DatabaseError as e:
            raise DatabaseError(f"Database error: {e}")

        finally:
            cursor.close()
            connection.close()                  

#Functions class which deals with Functions Table
class Functions:
    def __init__(self, user_id,eventid):
        self.user_id = user_id
        self.eventid = eventid

    def add_Function(self):
        try:
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                cursor.execute('INSERT INTO  Function (UserID,EventTypeID) VALUES (?,?)', (self.user_id,self.eventid))    

        except sqlite3.OperationalError as e:
            raise DatabaseError("There was an operational error.")

        except sqlite3.DatabaseError as e:
            raise DatabaseError(f"Database error: {e}")

        finally:
            cursor.close()
            connection.close()                      

    def update(self):
        try:
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                query = '''
                UPDATE Function
                SET EventTypeID= ?
                WHERE UserID = ?
                '''
                parameters = (self.eventid, self.user_id)
                cursor.execute(query, parameters)
                connection.commit()     

        except sqlite3.OperationalError as e:
            raise DatabaseError("There was an operational error.")

        except sqlite3.DatabaseError as e:
            raise DatabaseError(f"Database error: {e}")

        finally:
            cursor.close()
            connection.close()                              

    def delete(userid):
        success = False
        try:    
            with sqlite3.connect('database.db') as connection:
                    cursor = connection.cursor()
                    cursor.execute(f"DELETE FROM User WHERE UserID = {userid}")
                    cursor.execute(f"DELETE FROM Function WHERE UserID = {userid}")
                    cursor.execute(f"DELETE FROM Payment WHERE UserID = {userid}")                                        
                    cursor.execute(f"DELETE FROM Hash WHERE UserID = {userid}")
                    success = True 
            return success
        
        except sqlite3.OperationalError as e:
            raise DatabaseError("There was an operational error.")

        except sqlite3.DatabaseError as e:
            raise DatabaseError(f"Database error: {e}")

        finally:
            cursor.close()
            connection.close()     

#Payment class which inserts into Payment Table
class Payment:
    def __init__(self, user_id,post_code, address_line,payment_method, price):
        self.user_id = user_id
        self.post_code = post_code
        self.address_line = address_line
        self.payment_method = payment_method
        self.price = price


    def add_Payment(self):
        try:
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                cursor.execute('INSERT INTO  Payment (UserID,PaymentMethod,AddressLine,PostCode,Price) VALUES (?,?,?,?,?)', (self.user_id, self.payment_method, self.address_line, self.post_code, self.price))
                connection.commit()

        except sqlite3.OperationalError as e:
            raise DatabaseError("There was an operational error.")

        except sqlite3.DatabaseError as e:
            raise DatabaseError(f"Database error: {e}")

        finally:
            cursor.close()
            connection.close()                     

    @classmethod
    def update(cls, address_line, post_code, userid):
        try:
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                query = '''
                UPDATE Payment
                SET AddressLine= ?, PostCode = ?
                WHERE UserID = ?
                '''
                parameters = (address_line,post_code, userid)
                cursor.execute(query, parameters)
                connection.commit()     

        except sqlite3.OperationalError as e:
            raise DatabaseError("There was an operational error.")

        except sqlite3.DatabaseError as e:
            raise DatabaseError(f"Database error: {e}")

        finally:
            cursor.close()
            connection.close()                  

#Clashed class which checks for unavailable bookings
class Clashed:
    def __init__(self,time, date):
        self.time = time
        self.date = date
    
    @classmethod
    def clashed(cls, time, date):
        try:
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                cursor.execute(f'SELECT * FROM User u JOIN Hash t ON u.UserID = t.UserID WHERE time = "{time}" AND date = "{date}"')
                result = cursor.fetchone()
                if result is not None:
                    return True
                else:
                    return False
                
        except sqlite3.OperationalError as e:
            raise DatabaseError("There was an operational error.")

        except sqlite3.DatabaseError as e:
            raise DatabaseError(f"Database error: {e}")

        finally:
            cursor.close()
            connection.close()      

#Hash class which performs the hash algorithm and deals with the Hash Table
class Hash:    
    def __init__(self, time,date, userid):
        self.time = time 
        self.date = date
        self.userid = userid


    def __hash_algorithm(self):
        hashvalue = f'{self.date}{self.userid}{self.time}'
        hashvalue = re.sub(r'[-:]', '', hashvalue)
        array = [0] * 20
        initial_values = [2,3]
        digest = ''
        for index, character in enumerate(hashvalue):
            ascii_value = ord(character)
            for i in range (20):
                initial_value = initial_values[i % len(initial_values)]
                value = (array[i] + ascii_value * (index + 1) + i )   
                value = (value * initial_value) % 256
                array[i] = value
        #converting into hexadecimal whilst removing the 0x at the front
        for number in array:
            digest += f'{number:x}'
        return digest

    def add_digest(self):
        digest = self.__hash_algorithm()
        try:
            #storing the digest in the Hash Table along with UserID,Time and Date
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                cursor.execute(f"""SELECT Time,Date FROM Hash WHERE Digest = '{digest}' """)
                existing = cursor.fetchone()
                if existing is not None:
                    cursor.execute(f"""
                        UPDATE Hash 
                        SET UserID = {self.userid}, Time = {self.time}, Date = {self.date} 
                        WHERE Digest = '{digest}' AND Date < CURRENT_DATE """)
                    row_deleted = cursor.rowcount()
                    if row_deleted < 0:
                        rehash = Hash(time = self.time, date = self.date, userid = digest)
                        rehash.update()
                    else:
                        print('Hash updated.')
                else:
                    cursor.execute('INSERT INTO  Hash (UserID,Digest,Time,Date) VALUES (?,?,?,?)', (self.userid, digest, self.time, self.date))
                    connection.commit()
            return digest
        
        except sqlite3.OperationalError as e:
            raise DatabaseError("There was an operational error.")

        except sqlite3.DatabaseError as e:
            raise DatabaseError(f"Database error: {e}")

        finally:
            cursor.close()
            connection.close()              
    
    def update(self):
        newdigest = self.__hash_algorithm()
        try:
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                cursor.execute(f"""SELECT Time,Date FROM Hash WHERE Digest = '{newdigest}' """)
                existing = cursor.fetchone()
                if existing is not None:
                    cursor.execute(f"""
                        UPDATE Hash 
                        SET UserID = {self.userid}, Time = {self.time}, Date = {self.date} 
                        WHERE Digest = '{newdigest}' AND Date < CURRENT_DATE """)
                    row_deleted = cursor.rowcount()
                    if row_deleted < 0:
                        rehash = Hash(time = self.time, date = self.date, userid = newdigest)
                        rehash.update()
                    else:
                        print('Hash updated.')
                else:
                    query = '''
                    UPDATE Hash
                    SET Digest = ?, Time = ?, Date = ?
                    WHERE UserID = ? 
                    '''
                    parameters = (newdigest, self.time, self.date, self.userid)
                    cursor.execute(query, parameters)
                connection.commit()        

        except sqlite3.OperationalError as e:
            print(f'{e}')
            raise DatabaseError("There was an operational error.")
        
        except sqlite3.DatabaseError as e:
            print(f'{e}')
            raise DatabaseError(f"Database error: {e}")

        finally:
            cursor.close()
            connection.close()      
        return newdigest
            
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

        except UnboundLocalError as e:
            raise UnboundLocalErrors(f"Unbound local error: {e}")
        
        except (socket.gaierror, socket.herror, socket.timeout, smtplib.SMTPException) as e:
                raise SocketError("The email server could not connect.")
        
        except Exception as e:
            raise ServerError("Unexpected error: {e}")
    
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

        except UnboundLocalError as e:
            raise UnboundLocalErrors(f"Unbound local error: {e}")
        
        except (socket.gaierror, socket.herror, socket.timeout, smtplib.SMTPException) as e:
                raise SocketError("The email server could not connect.")
        
        except Exception as e:
            raise ServerError("Unexpected error: {e}")

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
            
            elif key == 'Event Type' or key == 'Payment Method':
                if value == '':
                    errors.append(f'Please select one of the {key} option.')

            elif key == 'Number Of People':
                if not value.isnumeric():
                    errors.append(f'{value} has to be a number')

            elif key == 'Child Date of Birth':
                match = re.match(r"""^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$""", value)
                if not match:
                    errors.append(f'{key} must be filled in.')
                else:
                    childdob = datetime.strptime(value, '%Y-%m-%d') 

                    start_date = datetime.strptime('2006-01-01', '%Y-%m-%d')
                    end_date = datetime.strptime('2016-12-31', '%Y-%m-%d')

                    if not (start_date <= childdob <= end_date):
                        errors.append(f"Child cannot attend this madrasash.")

            elif key == 'Email':
                match = re.match(r"""^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$""", value)
                if not match:
                    errors.append(f"{key} must be a valid email")


            elif key == 'Post Code' or key == 'Address Line':
                if not (value.replace(' ','')).isalnum():
                    errors.append(f"{key} must not contain special characters.")

            else:
                match = re.match(r"""^(?![\s.]+$)[a-zA-Z\s.]+$""", value)
                if not match:
                    errors.append(f"{key} must be alphabetical characters.")
                    
        if errors:
            errors = '\n'.join(errors)
            return errors 


# CREATE TABLE "User" (
#     "UserID"	INTEGER,
#     "FirstName"	VARCHAR(50) NOT NULL,
#     "LastName"	VARCHAR(50) NOT NULL,
#     "Email"	VARCHAR(255) NOT NULL,
#     "PhoneNumber"	VARCHAR(11) NOT NULL,
#     "DoB"	DATE,
#     PRIMARY KEY("UserID" AUTOINCREMENT)
# );

# CREATE TABLE "Hash" (
#     "Digest"	TEXT NOT NULL UNIQUE,
#     "UserID"	INTEGER NOT NULL,
#     "Time"	TEXT NOT NULL,
#     "Date"	DATE NOT NULL,
#     PRIMARY KEY("Digest"),
#     FOREIGN KEY("UserID") REFERENCES "User"("UserID")
# );                                

# CREATE TABLE "Nikah" (
#     "NikahID"	INTEGER,
#     "UserID"	INTEGER NOT NULL,
#     "GroomFirstName"	VARCHAR(50) NOT NULL,
#     "GroomLastName"	VARCHAR(50) NOT NULL,
#     "BrideFirstName"	VARCHAR(50) NOT NULL,
#     "BrideLastName"	VARCHAR(50) NOT NULL,
#     PRIMARY KEY("NikahID" AUTOINCREMENT),
#     FOREIGN KEY("UserID") REFERENCES "User"("UserID")
# );

# CREATE TABLE "Madrasah" (
#     "MadrasahID"	INTEGER,
#     "UserID"	INTEGER NOT NULL,
#     "ChildFirstName"	VARCHAR(50) NOT NULL,
#     "ChildLastName"	VARCHAR(50) NOT NULL,
#     "ChildDoB"	DATE NOT NULL,
#     PRIMARY KEY("MadrasahID" AUTOINCREMENT),
#     FOREIGN KEY("UserID") REFERENCES "User"("UserID")
# );

# CREATE TABLE "Tours" (
#     "TourID"	INTEGER,
#     "UserID"	INTEGER NOT NULL,
#     "NumberOfPeople"	INTEGER NOT NULL,
#     "EventTypeID"	INTEGER NOT NULL,
#     PRIMARY KEY("TourID" AUTOINCREMENT),
#     FOREIGN KEY("EventTypeID") REFERENCES "EventType"("EventTypeID"),
#     FOREIGN KEY("UserID") REFERENCES "User"("UserID")
# );    

# CREATE TABLE "Function" (
#     "FunctionID"	INTEGER,
#     "UserID"	INTEGER NOT NULL,
#     "EventTypeID"	INTEGER NOT NULL,
#     PRIMARY KEY("FunctionID" AUTOINCREMENT),
#     FOREIGN KEY("EventTypeID") REFERENCES "EventType"("EventTypeID"),
#     FOREIGN KEY("UserID") REFERENCES "User"("UserID")
# );        

# CREATE TABLE "Payment" (
#     "PaymentID"	INTEGER,
#     "UserID"	INTEGER NOT NULL,
#     "PaymentMethod"	VARCHAR(10) NOT NULL,
#     "AddressLine"	VARCHAR(25) NOT NULL,
#     "PostCode"	VARCHAR(25) NOT NULL,
#     "Price"	INTEGER NOT NULL,
#     PRIMARY KEY("PaymentID" AUTOINCREMENT),
#     FOREIGN KEY("UserID") REFERENCES "User"("UserID")
# );

# CREATE TABLE "EventType" (
#     "EventTypeID"	INTEGER,
#     "EventType"	VARCHAR(50),
#     PRIMARY KEY("EventTypeID")
# );
