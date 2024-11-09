import sqlite3
#User class which inserts into User Table
class User:
    def __init__(self, first_name, last_name, email, phone_number, date_of_birth):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.date_of_birth= date_of_birth
    
    def add(self):
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

    def add(self):
        with sqlite3.connect('test2.db') as conn:
             cursor = conn.cursor()
             cursor.execute('INSERT INTO  Nikah (UserID,GroomFirstName,GroomLastName,BrideFirstName,BrideLastName,Time, Date, PostCode,AddressLine) VALUES (?,?,?,?,?,?,?,?,?)', (self.user_id, self.groom_first_name,self.groom_last_name, self.bride_first_name, self.bride_last_name, self.time, self.date, self.post_code, self.address_line))

             conn.commit()  
#Payment class which inserts into Payment Table
class Payment:
    def __init__(self, user_id,post_code, address_line,payment_method, CVC, price):
        self.user_id = user_id
        self.post_code = post_code
        self.address_line = address_line
        self.payment_method = payment_method
        self.CVC = CVC
        self.price = price


    def add(self):
        with sqlite3.connect('test2.db') as conn:
             cursor = conn.cursor()
             cursor.execute('INSERT INTO  Payment (UserID,PaymentMethod,AddressLine,PostCode,CVC, Price) VALUES (?,?,?,?,?,?)', (self.user_id, self.payment_method, self.address_line, self.post_code, self.CVC, self.price))
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

    def add(self):
        with sqlite3.connect('test2.db') as conn:
             cursor = conn.cursor()
             cursor.execute('INSERT INTO  Madrasah (UserID,Time, Date, ChildFirstName,ChildLastName ,ChildDoB) VALUES (?,?,?,?,?,?)', (self.user_id,self.time,self.date,self.child_fname,self.child_lname,self.child_date_of_birth ))
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
                    print(e)
        return exists 