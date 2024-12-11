from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import User, Nikah, Payment,Madrasah, Clashed
import sqlite3

testing_bp = Blueprint('testing', __name__)

#Home Page
@testing_bp.route('/')
def home_page():
    return render_template("pages/home_page.html")

#Route to the Nikah Page
@testing_bp.route('/nikah')
def nikah_page():
    return render_template("pages/nikah_page.html")

#Route to the Madrasah Page
@testing_bp.route('/madrasah')
def madrasah_page():
    return render_template("pages/madrasah_page.html")

# Route to the Nikah Form 
@testing_bp.route("/nikahbooking")
def nikah_booking():
    return render_template("forms/nikah_form.html")

#Route to the Madrasah Form
@testing_bp.route("/madrasahbooking")
def madrasah_booking():
    return render_template("forms/madrasah_form.html")

#Development needed
@testing_bp.route("/verification", methods = ['POST'])
def verification():
    print("Working pls?")
    return render_template("pages/home_page.html")

#Process for Nikah Table which retrieves the input from the nikah_form.
@testing_bp.route("/process-nikah", methods=['GET','POST'])
def addnikah():
    if request.method == 'POST':        
        time = request.form["time"]
        date = request.form["date"]
        #checking for any bookings that could clash using the class Clashed
        if Clashed.clashed(time, date):
            flash(f'Unfortunately this booking on {date} at {time} is unavailable. Please re-book for another time/date.', 'error')
            return redirect(url_for('testing.addnikah'))
        else:
            #requesting data from the nikah_form             
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            groom_first_name = request.form["groom_first_name"]               
            groom_last_name = request.form["groom_last_name"]               
            bride_first_name = request.form["bride_first_name"]               
            bride_last_name = request.form["bride_last_name"]               
            email = request.form["email"]                
            phone_number = request.form["phone_number"]               
            date_of_birth = request.form["date_of_birth"]               
            post_code = request.form["post_code"]            
            address_line = request.form["address_line"]             
            payment_method = request.form.get('payment_method')            
            cvc = request.form["CVC"]
            price = 130
            print(f'this is the values: {groom_first_name}, {groom_last_name}, {bride_first_name}, {bride_last_name}')
            #using the class User to store the data for the User Table
            new_user = User(first_name = first_name, last_name= last_name, email = email, phone_number= phone_number, date_of_birth= date_of_birth )
            new_user.add()
            
            #retrieving the correct coressponding UserID 
            connection = sqlite3.connect('test2.db')
            cursor = connection.cursor()
            cursor.execute('SELECT seq FROM sqlite_sequence WHERE name="User"')
            result = cursor.fetchone()
            user_id = result[0]
            connection.commit()
            cursor.close()
            
            #calling the class Nikah to store the data for the Nikah Table
            new_nikah = Nikah(user_id= user_id,groom_first_name= groom_first_name , groom_last_name= groom_last_name , bride_first_name=bride_first_name , bride_last_name=bride_last_name ,time= time, date= date, post_code= post_code, address_line= address_line)
            new_nikah.add()  
            
            #calling the class Payment to store the data for the Payment Table
            new_payment = Payment(user_id= user_id, post_code= post_code, address_line= address_line, CVC= cvc, payment_method= payment_method, price = price)
            new_payment.add()
                
            return render_template("success.html")
    else:
        return redirect(url_for('testing.nikah_booking'))


#Process for Madrasah Table which retrieves the user input from the madrasah_form
@testing_bp.route("/process-madrasah", methods=['GET','POST'])
def addmadrasah():
    if request.method == 'POST':        
        time = request.form["time"]
        date = request.form["date"]
        #checking for any bookings that could clash
        print(f'the result is : {Clashed.clashed(time,date)}')

        if Clashed.clashed(time, date):
            flash(f'Unfortunately this booking on {date} at {time} is unavailable. Please re-book for another time/date.', 'clashed')
            return redirect(url_for('testing.addmadrasah'))
        
        else:
            #requesting data from the madrasah_form             
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]               
            email = request.form["email"]                
            phone_number = request.form["phone_number"]
            date_of_birth = request.form["date_of_birth"]               
            child_fname = request.form["child_fname"]
            child_lname = request.form["child_lname"]
            child_date_of_birth = request.form["child_date_of_birth"]               


            #calling the class User and storign the data for the User Table
            new_user = User(first_name = first_name, last_name= last_name, email = email, phone_number= phone_number, date_of_birth= date_of_birth)
            new_user.add()
            #retrieving the correct coressponding UserID 
            connection = sqlite3.connect('test2.db')
            cursor = connection.cursor()
            cursor.execute('SELECT seq FROM sqlite_sequence WHERE name="User"')
            result = cursor.fetchone()
            user_id = result[0]
            connection.commit()
            cursor.close()
            
            #calling the class Madrasah and storing the data for the Madrasah Table 
            new_madrasah = Madrasah(user_id= user_id, time= time, date= date, child_fname = child_fname , child_lname = child_lname ,child_date_of_birth= child_date_of_birth )
            new_madrasah.add()  
                
            return render_template("success.html")
    else:
        return redirect(url_for('testing.madrasah_booking'))    