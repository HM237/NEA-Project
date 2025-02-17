import os
import sqlite3
from flask import Flask
from blueprints import bp

#Stating the database file path
DATABASE = os.path.join(os.path.dirname(__file__), 'database.db')

def database__init__():
    # Checks whether database exists in directory.
    if not os.path.exists(DATABASE):
        print("Database does not exist. Creating a new database...")
        
        #if it doesn't exist we will then have to create the tables.
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Creating User Table
        cursor.execute("""
            CREATE TABLE "User" (
                "UserID"	INTEGER,
                "FirstName"	VARCHAR(50) NOT NULL,
                "LastName"	VARCHAR(50) NOT NULL,
                "Email"	VARCHAR(255) NOT NULL,
                "PhoneNumber"	VARCHAR(11) NOT NULL,
                "DoB"	DATE,
                PRIMARY KEY("UserID" AUTOINCREMENT)
            ); """)
        
        # Creating Hash Table
        cursor.execute("""
            CREATE TABLE "Hash" (
                "Digest"	TEXT NOT NULL,
                "UserID"	INTEGER NOT NULL,
                "Time"	TEXT NOT NULL,
                "Date"	DATE NOT NULL,
                PRIMARY KEY("Digest"),
                FOREIGN KEY("UserID") REFERENCES "User"("UserID")
            ); """)
        
        # Creating Nikah Table        
        cursor.execute("""
            CREATE TABLE "Nikah" (
                "NikahID"	INTEGER,
                "UserID"	INTEGER NOT NULL,
                "GroomFirstName"	VARCHAR(50) NOT NULL,
                "GroomLastName"	VARCHAR(50) NOT NULL,
                "BrideFirstName"	VARCHAR(50) NOT NULL,
                "BrideLastName"	VARCHAR(50) NOT NULL,
                PRIMARY KEY("NikahID" AUTOINCREMENT),
                FOREIGN KEY("UserID") REFERENCES "User"("UserID")
            ); """)

        # Creating Madrasah Table
        cursor.execute("""
            CREATE TABLE "Madrasah" (
                "MadrasahID"	INTEGER,
                "UserID"	INTEGER NOT NULL,
                "ChildFirstName"	VARCHAR(50) NOT NULL,
                "ChildLastName"	VARCHAR(50) NOT NULL,
                "ChildDoB"	DATE NOT NULL,
                PRIMARY KEY("MadrasahID" AUTOINCREMENT),
                FOREIGN KEY("UserID") REFERENCES "User"("UserID")
            );""")

        # Creating Tours Table
        cursor.execute("""
            CREATE TABLE "Tours" (
                "TourID"	INTEGER,
                "UserID"	INTEGER NOT NULL,
                "NumberOfPeople"	INTEGER NOT NULL,
                "EventTypeID"	INTEGER NOT NULL,
                PRIMARY KEY("TourID" AUTOINCREMENT),
                FOREIGN KEY("EventTypeID") REFERENCES "EventType"("EventTypeID"),
                FOREIGN KEY("UserID") REFERENCES "User"("UserID")
            );""")
        
        # Creating Function Table        
        cursor.execute("""
            CREATE TABLE "Function" (
                "FunctionID"	INTEGER,
                "UserID"	INTEGER NOT NULL,
                "EventTypeID"	INTEGER NOT NULL,
                PRIMARY KEY("FunctionID" AUTOINCREMENT),
                FOREIGN KEY("EventTypeID") REFERENCES "EventType"("EventTypeID"),
                FOREIGN KEY("UserID") REFERENCES "User"("UserID")
            );""")
        
        cursor.execute("""
            CREATE TABLE "Payment" (
                "PaymentID"	INTEGER,
                "UserID"	INTEGER NOT NULL,
                "PaymentMethod"	VARCHAR(10) NOT NULL,
                "AddressLine"	VARCHAR(25) NOT NULL,
                "PostCode"	VARCHAR(25) NOT NULL,
                "Price"	INTEGER NOT NULL,
                PRIMARY KEY("PaymentID" AUTOINCREMENT),
                FOREIGN KEY("UserID") REFERENCES "User"("UserID")
            );""")        

        # Creating EventType Table
        cursor.execute("""
            CREATE TABLE "EventType" (
                "EventTypeID"	INTEGER,
                "EventType"	VARCHAR(50),
                PRIMARY KEY("EventTypeID")
            );""")
        
        #Inser the event types into EventType Table
        EventTypes = [
            ('Aqiqah',),
            ('Walimah',),
            ('Educational',),
            ('Community Engagement',),
            ('Other',)
        ]
        
        cursor.executemany(""" INSERT INTO EventType (EventType) VALUES (?) """, EventTypes)

        # Commit changes and close the connection
        conn.commit()
        conn.close()
        print("Database and tables created successfully.")
    else:
        print("Database already exists.")

def app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE = DATABASE
    )

    database__init__()

    app.register_blueprint(bp)

    return app


if __name__ == "__main__":
    app.debug = True
    app().run()

#netstat -ano | findstr :5000
#taskkill /PID 2660 /F
