from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from models import User, Nikah, Madrasah,Payment, Clashed, Verification
import sqlite3

bp = Blueprint('routes', __name__)

#Route to the Home Page
@bp.route('/')
def index():
    return render_template("pages/index.html")

#Route to the About Us Page
@bp.route('/about-us')
def aboutus_page():
    return render_template("pages/aboutus_page.html")


#Route to the Temporary Page
@bp.route('/temporary')
def temporary():
    form_id = "NikahForm"
    action_url = url_for('routes.addnikah')
    return render_template("forms/temporary.html", form_id=form_id, action_url=action_url)

#Route to the FAQ Page
@bp.route('/faq')
def faq_page():
    return render_template("pages/faq_page.html")

#Route to the Nikah Page
@bp.route('/prayer-timetable')
def prayertime_page():
    return render_template("pages/prayertime_page.html")

#Route to the Nikah Page
@bp.route('/nikah')
def nikah_page():
    return render_template("pages/nikah_page.html")

#Route to the Madrasah Page
@bp.route('/madrasah')
def madrasah_page():
    return render_template("pages/madrasah_page.html")

#Route to the Tours Page
@bp.route('/tours')
def tours_page():
    return render_template("pages/tours_page.html")

#Route to the Service Page
@bp.route('/service')
def service_page():
    return render_template("pages/service_page.html")

# Route to the Nikah Form 
@bp.route("/nikahbooking")
def nikah_booking():
    #Filling in the formId and actionURL for the forms
    form_id = "NikahForm"
    action_url = url_for('routes.addnikah')
    return render_template("forms/nikah_form.html", form_id=form_id, action_url=action_url)

#Route to the Madrasah Form
@bp.route("/madrasahbooking")
def madrasah_booking():
    form_id = "MadrasahForm"
    action_url = url_for('routes.addmadrasah')
    return render_template("forms/madrasah_form.html", form_id=form_id, action_url=action_url)

#Development needed REVERIFICATION?
@bp.route("/verification", methods = ['GET','POST'])
def verification():
    referrer = request.referrer  # The URL that made the request (previous page URL)
    current_url = request.url  # The URL of the current request
    verification_number = None

    if request.method == 'POST':
        email = request.form.get('email')
        time = request.form.get('time')
        date = request.form.get('date')
        print(f'this is the time {time} and {date}\nand email: {email}')
        
        #email = request.form['email']
        #time = request.form["time"] 
        #date = request.form["date"]

        #checking for any bookings that could clash using the class Clashed and then flashing the message
        if Clashed.clashed(time, date):
            return jsonify({"message": f"Unfortunately this booking on {date} at {time} is unavailable. Please re-book for another time/date.'"})
        else:
            #sends the user's email to the class Verification
            user_email = Verification(email= email)
            #send both the email and is given the verification number that was sent to user
            verification_number = user_email.send_verification_email()
            return jsonify({"message": f"Verification email sent successfully, please check your inbox!'"})


#    checking_email = Verification(email= email)
#    verification_number = checking_email.send_verification_email()
    print(f'this is the verification_number: {verification_number}')
    
    
    flash('Verification email sent successfully, please check your inbox!', 'success')

    return render_template("email.html")
#Process for Nikah Table which retrieves the input from the nikah_form.
@bp.route("/process-nikah", methods=['GET','POST'])
def addnikah():
    if request.method == 'POST':        
        time = request.form["time"] 
        date = request.form["date"]
        #checking for any bookings that could clash using the class Clashed and then flashing the message
        if Clashed.clashed(time, date):
            flash(f'Unfortunately this booking on {date} at {time} is unavailable. Please re-book for another time/date.', 'error')
            return redirect(url_for('routes.addnikah'))
        else:
            #retrieving data from the nikah_form             
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
            #using the class User to store the data for the User Table
            new_user = User(first_name = first_name, last_name= last_name, email = email, phone_number= phone_number, date_of_birth= date_of_birth )
            new_user.add_User()
            
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
            new_nikah.add_Nikah()  
            
            #calling the class Payment to store the data for the Payment Table
            new_payment = Payment(user_id= user_id, post_code= post_code, address_line= address_line, CVC= cvc, payment_method= payment_method, price = price)
            new_payment.add_Payment()
                
            return render_template("success.html")
    else:
        return redirect(url_for('routes.nikah_booking'))


#Process for Madrasah Table which retrieves the user input from the madrasah_form
@bp.route("/process-madrasah", methods=['GET','POST'])
def addmadrasah():
    if request.method == 'POST':        
        time = request.form["time"]
        date = request.form["date"]
        #checking for any bookings that could clash
        if Clashed.clashed(time, date):
            flash(f'Unfortunately this booking on {date} at {time} is unavailable. Please re-book for another time/date.', 'clashed')
            return redirect(url_for('routes.addmadrasah'))
        
        else:
            #retrieving data from the madrasah_form             
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
            new_user.add_User()
            
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
            new_madrasah.add_Madrasah()  
                
            return render_template("success.html")
    else:
        return redirect(url_for('routes.madrasah_booking'))    
###basically after adding the json what now happens is that in the Nikah form all the required fields do not work HOWEVER the madrasah fields still work. Weird thing fr. we will need to debug this dumb thing and see why it happens