from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from models import User, Nikah, Madrasah,Payment, Clashed, Email, Hash
import sqlite3
import random


bp = Blueprint('routes', __name__)

#Route to the Temporary Page
@bp.route('/temporary')
def temporary():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM User u JOIN Nikah t ON u.UserID = t.UserID WHERE u.UserID=64")

    rows = cur.fetchall()
    con.close()
    return render_template("tables/nikah_table.html", rows = rows)

#Route to the Home Page
@bp.route('/')
def index():
    return render_template("pages/index.html")

#Route to the About Us Page
@bp.route('/about-us')
def aboutus_page():
    return render_template("pages/aboutus_page.html")


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
    #here we are generating a random 6 digit number which will act as our verification code. We then use Flask session to store this number for this session. This will allow me to compare the verification-code the user submits and see whether or not it is the correct one.
    random_number = random.randint(111111,999999)
    session['random_number'] = random_number

    if request.method == 'POST':
        email = request.form.get('email')
        time = request.form.get('time')
        date = request.form.get('date')
        #print(f'Verification\ntime,date:{time, date}\nemail:{email}')
        #checking for any bookings that could clash using the class Clashed and then flashing the message
        if Clashed.clashed(time, date):
            return jsonify({"message": f"Unfortunately this booking on {date} at {time} is unavailable. Please re-book for another time/date.'"})
        else:
            #sends the user's email and the random number we generate to the class Email
            user_email = Email(email= email, number = random_number)
            #sending the email containg the verification code.
            verification_email = user_email.send_verification_email()
            return jsonify({"message": f"Verification email sent successfully, please check your email inbox!'"})

    

    return render_template("pages/tours_page.html")



#Process for Nikah Table which retrieves the input from the nikah_form.
@bp.route("/process-nikah", methods=['GET','POST'])
def addnikah():
    random_number = session.get('random_number') # Retrieve the stored random number in our session    
    if random_number:
        print(f'The verification code generated: {random_number}')
    else:
        return jsonify({"message": f"Please press the 'Send Verifcation' button to send the code to your box first!"})
    
    
    if request.method == 'POST':        
        time = request.form["time"] 
        date = request.form["date"]
        #checking for any bookings that could clash using the class Clashed and then flashing the message
        if Clashed.clashed(time, date):
            return jsonify({"message": f"Unfortunately this booking on {date} at {time} is unavailable. Please re-book for another time/date.'"})
        else:
            #now verifying if the user submiited the right verification code
            verification_code = request.form["verification-code"]
            if int(verification_code) != random_number:
                return jsonify({"message": f"Unfortunately this was not the correct code. Please try again!"}) #error message if they did not
            else:
                session.pop('random_number', None) # we will remove the number from session as it is now void
            
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
            price = 130

            ### print statement to print all the form details
            # print(f'nikah\nverificationcode: {verification_code}\nfirst: {first_name}\nsecond:{ last_name}\nemail: {email}\nphone: {phone_number}\ndob: {date_of_birth}\ngroom:   {groom_first_name}\ngroonl: {groom_last_name}\ncvc: {cvc}')

            #using the class User to store the data for the User Table
            new_user = User(first_name = first_name, last_name= last_name, email = email, phone_number= phone_number, date_of_birth= date_of_birth )
            new_user.add_User()
            

            with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    cur.execute('SELECT seq FROM sqlite_sequence WHERE name="User"')
                    result = cur.fetchone()
                    userid = result[0]
                    con.commit()
                    cur.close()
            
            #calling the class Nikah to store the data for the Nikah Table
            new_nikah = Nikah(user_id= userid,groom_first_name= groom_first_name , groom_last_name= groom_last_name , bride_first_name=bride_first_name , bride_last_name=bride_last_name ,time= time, date= date, post_code= post_code, address_line= address_line)
            new_nikah.add_Nikah()  
            
            #calling the class Payment to store the data for the Payment Table
            new_payment = Payment(user_id= userid, post_code= post_code, address_line= address_line, payment_method= payment_method, price = price)
            new_payment.add_Payment()

            #sending the summary email after inserting all data to database
            user_email = Email(email= email, number=(Hash.hash_algorithm(time, date, userid)))
            summary_email = user_email.send_summary_email()

                
            return jsonify({"message": f"Booking was successful, please check your email inbox for summary email!!'"}) #success message 
    else:
        return redirect(url_for('routes.nikah_booking'))



#Process for Madrasah Table which retrieves the user input from the madrasah_form
@bp.route("/process-madrasah", methods=['GET','POST'])
def addmadrasah():
    #same comments as line 102
    random_number = session.get('random_number') # Retrieve and remove the stored random number
    if random_number:
        print(f'The verification code generated: {random_number}')
    else:
        return jsonify({"message": f"Please press the 'Send Verifcation' button to send the code to your box first!"})    
    if request.method == 'POST':        
        time = request.form["time"]
        date = request.form["date"]
        #checking for any bookings that could clash
        if Clashed.clashed(time, date):
            return jsonify({"message": f"Unfortunately this booking on {date} at {time} is unavailable. Please re-book for another time/date.'"})
        
        else:
            verification_code = request.form["verification-code"]
            #checks the verification code is all numbers/ if it even is the right code
            if (not verification_code.isnumeric()) or (int(verification_code) != random_number):
                return jsonify({"message": f"Unfortunately this was not the correct code. Please try again!"})
            else:
                session.pop('random_number', None)
            
            #retrieving data from the madrasah_form             
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]               
            email = request.form["email"]                
            phone_number = request.form["phone_number"]
            date_of_birth = request.form["date_of_birth"]               
            child_fname = request.form["child_fname"]
            child_lname = request.form["child_lname"]
            child_date_of_birth = request.form["child_date_of_birth"]

            # print statement for the entire form
            # print(f'Madrasahn\nverificationcode: {verification_code}\nfirst: {first_name}\nsecond: {last_name}\nemail: {email}\nphone: {phone_number}\ndob: {date_of_birth}\nchild:{child_fname}\nchildl: {child_lname}\nchilddob: {child_date_of_birth}')

            #calling the class User and storign the data for the User Table
            new_user = User(first_name = first_name, last_name= last_name, email = email, phone_number= phone_number, date_of_birth= date_of_birth)
            new_user.add_User()
            
            with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    cur.execute('SELECT seq FROM sqlite_sequence WHERE name="User"')
                    result = cur.fetchone()
                    userid = result[0]
                    con.commit()
                    cur.close()
            
            #calling the class Madrasah and storing the data for the Madrasah Table 
            new_madrasah = Madrasah(user_id= userid, time= time, date= date, child_fname = child_fname , child_lname = child_lname ,child_date_of_birth= child_date_of_birth )
            new_madrasah.add_Madrasah()  
            
            #sending the summary email after inserting all data to database    
            user_email = Email(email= email, number=(Hash.hash_algorithm(time, date, userid)))
            summary_email = user_email.send_summary_email()
            
            return jsonify({"message": f"Booking was successful, please check your email inbox for summary email!'"})
    else:
        return redirect(url_for('routes.madrasah_booking'))    

@bp.route('/booking/<digest>')
def booking(digest):
    return f"Booking details for: {digest}"

@bp.route("/edit", methods=['POST','GET'])
def edit():
    if request.method == 'POST':
        try:
            userid = request.form['userid']
            print(f'this was the id: {userid}')
            connection = sqlite3.connect("database.db")
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM User u JOIN Nikah t ON u.UserID = t.UserID WHERE u.UserID={userid}")
            rows = cursor.fetchall()
        except:
            userid=None
        finally:
            connection.close()
            return render_template("forms/edit_forms/editnikah.html",rows=rows)

@bp.route("/editrec", methods=['POST','GET'])
def editnikahbooking():
    print(f'hello')
    # Data will be available from POST submitted by the form
    if request.method == 'POST':
        time = request.form["time"] 
        date = request.form["date"]

        #checking for any bookings that could clash using the class Clashed and then flashing the message
        if Clashed.clashed(time, date):
            return jsonify({"message": f"Unfortunately this booking on {date} at {time} is unavailable. Please re-book for another time/date.'"})
        else:            
            #retrieving data from the edit nikah_form
            userid = request.form["UserID"]
            nikahid = request.form["NikahID"]
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            groom_first_name = request.form["groom_first_name"]               
            groom_last_name = request.form["groom_last_name"]               
            bride_first_name = request.form["bride_first_name"]               
            bride_last_name = request.form["bride_last_name"]               
            post_code = request.form["post_code"]            
            address_line = request.form["address_line"]   

            #where we send the editing data i=to the update in the class Nikah
            new_nikah = Nikah(groom_first_name= groom_first_name , groom_last_name= groom_last_name , bride_first_name=bride_first_name , bride_last_name=bride_last_name ,time= time, date= date, post_code= post_code, address_line= address_line, user_id=userid)
            new_nikah.update()  

            return jsonify({"message": f"CHANGE WAS SUCCESSFUL!!'"}) #success message 
    else:
        return redirect(url_for('routes.nikah_booking'))

@bp.route("/delete", methods=['POST','GET'])
def delete():
    if request.method == 'POST':
        try:
             # Use the hidden input value of id from the form to get the rowid
            userid = request.form['userid']
            # Connect to the database and DELETE a specific record based on rowid
            with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    cur.execute(F"DELETE FROM Nikah WHERE UserID={userid}")
                    cur.execute(F"PRAGMA foreign_keys = OFF DELETE FROM Nikah WHERE UserID = {userid}")
                    con.commit()
        except:
            con.rollback()
            msg = "Error in the DELETE"

        finally:
            con.close()
            # Send the transaction message to result.html
            return render_template("pages/nikah_page")



###basically after adding the json what now happens is that in the Nikah form all the required fields do not work HOWEVER the madrasah fields still work. Weird thing fr. we will need to debug this dumb thing and see why it happens