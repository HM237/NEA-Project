from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from models import User, Nikah, Madrasah,Tours,Payment, Clashed, Email, Hash, Validation
from datetime import datetime, timedelta
import sqlite3
import random
import re


bp = Blueprint('routes', __name__)

#Route to the Home Page
@bp.route('/')
def index():
    return render_template("pages/index.html")

#Route to the About Us Page
@bp.route('/about-us')
def aboutus():
    return render_template("pages/aboutus.html")


#Route to the FAQ Page
@bp.route('/faq')
def faq():
    return render_template("pages/faq.html")

#Route to the Nikah Page
@bp.route('/prayer-timetable')
def prayertime():
    return render_template("pages/prayertime.html")

#Route to the Nikah Page
@bp.route('/nikah')
def nikah():
    return render_template("pages/nikah.html")

#Route to the Madrasah Page
@bp.route('/madrasah')
def madrasah():
    return render_template("pages/madrasah.html")

#Route to the Tours Page
@bp.route('/tours')
def tours():
    return render_template("pages/tours.html")

#Route to the Service Page
@bp.route('/functions')
def functions():
    return render_template("pages/functions.html")










####################  Entire Verification Process ####################

#Development needed REVERIFICATION?
@bp.route("/verification/<service>", methods = ['GET','POST'])
def verification(service):
    #here we are generating a random 6 digit number which will act as our verification code. We then use Flask session to store this number for this session. This will allow me to compare the verification-code the user submits and see whether or not it is the correct one.
    random_number = random.randint(111111,999999)
    session['random_number'] = random_number

    if request.method == 'POST':
        email = request.form.get('email')
        match = re.match("""^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$""", email)
        if not match:
            session.pop('random_number', None)
            return jsonify({"message": f"PLease enter a valid email before trying to send a verification code."})

        time = request.form.get('time')
        date = request.form.get('date')
        #print(f'Verification\ntime,date:{time, date}\nemail:{email}')
        #checking for any bookings that could clash using the class Clashed and then flashing the message
        if Clashed.clashed(time, date) or (time == '') or (date==''):
            return jsonify({"message": f"Unfortunately this booking on {date} at {time} is unavailable. Please re-book for another time/date.'"})
        
        if service == 'nikah':
            #retrieving data from the nikah_form
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            groom_first_name = request.form["groom_first_name"]               
            groom_last_name = request.form["groom_last_name"]               
            bride_first_name = request.form["bride_first_name"]               
            bride_last_name = request.form["bride_last_name"]               
            email = request.form["email"]                            
            post_code = request.form["post_code"]            
            address_line = request.form["address_line"]              
                  
            data = {'First Name': first_name, 'Last Name': last_name, 'Groom First Name':groom_first_name, 'Groom Last Name': groom_last_name, 'Bride First Name': bride_first_name, 'Bride Last Name': bride_last_name,'Email':email ,"Address Line":address_line, 'Post Code':post_code, 'Time':time, 'Date': date}
            invalid = Validation.validate(data= data)
            if invalid:
                return jsonify({"message": f"{invalid}"}) #error message if they did not
            else:
                #sends the user's email and the random number we generate to the class Email
                user_email = Email(email= email, number = random_number)
                #sending the email containg the verification code.
                user_email.send_verification_email()
                return jsonify({"message": f"Verification email sent successfully, please check your email inbox!'"})       

        elif service =='madrasah':
            #retrieving data from the madrasah_form             
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]               
            email = request.form["email"]                
            child_fname = request.form["child_fname"]
            child_lname = request.form["child_lname"]
            child_date_of_birth = request.form["child_date_of_birth"]

            data = {'First Name':first_name, 'Last Name': last_name, 'Child First Name':child_fname, 'Child Last Name': child_lname, 'Child Date of Birth': child_date_of_birth, 'Email':email,'Time': time, 'Date':date}

            invalid = Validation.validate(data = data)
            if invalid:
                return jsonify({"message": f"{invalid}"}) #error message if they did not
            else:
                #sends the user's email and the random number we generate to the class Email
                user_email = Email(email= email, number = random_number)
                #sending the email containg the verification code.
                user_email.send_verification_email()
                return jsonify({"message": f"Verification email sent successfully, please check your email inbox!'"})       


        elif service == 'tour':
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]               
            email = request.form["email"]                               
            number_of_people = request.form["number_of_people"]

            data = {'First Name':first_name, 'Last Name': last_name, 'Number Of People':number_of_people, 'Email':email,'Time': time, 'Date':date}

            invalid = Validation.validate(data = data)
            if invalid:
                return jsonify({"message": f"{invalid}"}) #error message if they did not  
            else:
                #sends the user's email and the random number we generate to the class Email
                user_email = Email(email= email, number = random_number)
                #sending the email containg the verification code.
                user_email.send_verification_email()
                return jsonify({"message": f"Verification email sent successfully, please check your email inbox!'"})                  
        else:
            #sends the user's email and the random number we generate to the class Email
            user_email = Email(email= email, number = random_number)
            #sending the email containg the verification code.
            user_email.send_verification_email()
            return jsonify({"message": f"Verification email sent successfully, please check your email inbox!'"})

    

    return render_template("pages/tours.html")










####################  Entire Nikah Process ####################

# Route to the Nikah Form 
@bp.route("/nikahbooking")
def nikah_booking():
    #Filling in the formId and actionURL for the forms
    form_id = "NikahForm"
    action_url = url_for('routes.addnikah')
    service = "nikah"
    return render_template("forms/nikah_form.html", form_id=form_id, action_url=action_url, service = service )


#Process for Nikah Table which retrieves the input from the nikah_form.
@bp.route("/process-nikah", methods=['GET','POST'])
def addnikah():
    random_number = session.get('random_number') # Retrieve the stored random number in our session and if not prompt user to create one    
    if random_number:
        print(f'The verification code was generated: {random_number}')
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

            if not verification_code.isnumeric():
                session.pop('random_number', None) # we will remove the number from session as it is now void
                return jsonify({"message": f"Unfortunately this was not the correct code. Please try again!"}) #error message if they did not

            elif (int(verification_code) != random_number):
                session.pop('random_number', None) # we will remove the number from session as it is now void
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

            data = {'First Name': first_name, 'Last Name': last_name, 'Groom First Name':groom_first_name, 'Groom Last Name': groom_last_name, 'Bride First Name': bride_first_name, 'Bride Last Name': bride_last_name,'Email':email ,"Address Line":address_line, 'Post Code':post_code, 'Time':time, 'Date': date}
            invalid = Validation.validate(data= data)
            if invalid:
                return jsonify({"message": f"{invalid}"}) #error message if they did not

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

            #calculating the digest from the hash values. We are sending this to the class Hash, and receiving the digest in return.
            hashvalue = Hash(time = time, date = date, userid = userid)
            digest = hashvalue.hash_algorithm()
            digest = hashvalue.add_digest(digest)
            #sending the summary email after inserting all data to database
            user_email = Email(email= email, number=(digest))
            user_email.send_summary_email(service='nikah')

                
            return jsonify({"message": f"Booking was successful, please check your email inbox for summary email!!'"}) #success message 
    else:
        return redirect(url_for('routes.nikah_booking'))


@bp.route("/editnikahbooking", methods=['POST','GET'])
def editnikahbooking():
    if request.method == 'POST':
        time = request.form["time"] 
        date = request.form["date"]
        userid = request.form["UserID"]
    
        with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(f'SELECT Time,Date FROM Hash WHERE UserID={userid}')
                result = cur.fetchone()
                con.commit()
                cur.close()  

        #we are now checking whether or not they have changed their booking date because if they have we need to:
        # a) Check for any existing bookings that can clash whilst excluding the current booking they have
        # b) Change the digest and update it
        if ((time != result[0] or date != result[1]) and (Clashed.clashed(time, date) or time =='' or date =='')):
            return jsonify({"message": f"Unfortunately this booking is unavailable. Please re-book for another time/date.'"})
        else:            
            #retrieving data from the edit nikah_form
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]        
            phone_number = request.form["phone_number"]               
            date_of_birth = request.form["date_of_birth"]   
            groom_first_name = request.form["groom_first_name"]               
            groom_last_name = request.form["groom_last_name"]               
            bride_first_name = request.form["bride_first_name"]               
            bride_last_name = request.form["bride_last_name"]               
            post_code = request.form["post_code"]            
            address_line = request.form["address_line"]   

  
            data = {'First Name': first_name, 'Last Name': last_name, 'Groom First Name':groom_first_name, 'Groom Last Name': groom_last_name, 'Bride First Name': bride_first_name, 'Bride Last Name': bride_last_name, 'Email':email,"Address Line":address_line, 'Post Code':post_code, 'Time':time, 'Date': date}


            invalid = Validation.update(data= data)
            if invalid:
                return jsonify({"message": f"{invalid}"}) #error message if they did not

            #updating the digest since their time/date has changed
            if (time != result[0]) or (date != result[1]):
                hashvalue = Hash(time = time, date = date, userid = userid)
                newdigest = hashvalue.hash_algorithm()     
                updatehash = Hash(time = time, date=date, userid = userid)
                updatehash.update(newdigest= newdigest)       
                                    
                #sending them a new booking link
                user_email = Email(email= email, number= newdigest)
                user_email.send_summary_email(service = 'nikah')

                new_user = User(first_name = first_name, last_name= last_name, email = email, phone_number= phone_number, date_of_birth= date_of_birth )
                new_user.update(userid= userid)

                #updating the booking by sending it to the class Nikah
                new_nikah = Nikah(groom_first_name= groom_first_name , groom_last_name= groom_last_name , bride_first_name=bride_first_name , bride_last_name=bride_last_name ,time= time, date= date, post_code= post_code, address_line= address_line, user_id=userid)
                new_nikah.update()  

                return jsonify(redirect_url=url_for('routes.booking', service='nikah', digest=f'{newdigest}'))
            else:
                new_user = User(first_name = first_name, last_name= last_name, email = email, phone_number= phone_number, date_of_birth= date_of_birth )
                new_user.update(userid= userid) 

                new_nikah = Nikah(groom_first_name= groom_first_name , groom_last_name= groom_last_name , bride_first_name=bride_first_name , bride_last_name=bride_last_name ,time= time, date= date, post_code= post_code, address_line= address_line, user_id=userid)
                new_nikah.update()  

                with sqlite3.connect('database.db') as con:
                        cur = con.cursor()
                        cur.execute(f'SELECT Digest FROM Hash WHERE UserID={userid}')
                        result = cur.fetchone()
                        digest = result[0]
                        con.commit()
                        cur.close()  

                return jsonify(redirect_url=url_for('routes.booking', service='nikah', digest=f'{digest}'))


    else:
        return redirect(url_for('routes.nikah_booking'))










####################  Entire Madrasah Process ####################

#Route to the Madrasah Form
@bp.route("/madrasahbooking")
def madrasah_booking():
    form_id = "MadrasahForm"
    action_url = url_for('routes.addmadrasah')
    service = "madrasah"
    return render_template("forms/madrasah_form.html", form_id=form_id, action_url=action_url, service = service)

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
                session.pop('random_number', None)
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

            #calling the class User and storing the data for the User Table

            data = {'First Name':first_name, 'Last Name': last_name, 'Child First Name':child_fname, 'Child Last Name': child_lname, 'Child Date of Birth': child_date_of_birth, 'Email':email,'Time': time, 'Date':date}

            invalid = Validation.validate(data = data)
            if invalid:
                return jsonify({"message": f"{invalid}"}) #error message if they did not

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
            
            #calculating the digest from the hash values. We are sending this to the class Hash, and receiving the digest in return.            
            hashvalue = Hash(time = time, date = date, userid = userid)
            digest = hashvalue.hash_algorithm()
            digest = hashvalue.add_digest(digest)

            #sending the summary email after inserting all data to database    
            user_email = Email(email= email, number=(digest))
            user_email.send_summary_email(service='madrasah')
            
            return jsonify({"message": f"Booking was successful, please check your email inbox for summary email! Feel free to make another booking as well!'"})
    else:
        return redirect(url_for('routes.madrasah_booking'))    


@bp.route("/editmadrasahbooking", methods=['POST','GET'])
def editmadrasahbooking():
    if request.method == 'POST':
        time = request.form["time"] 
        date = request.form["date"]
        userid = request.form["UserID"]
    
        with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(f'SELECT Time,Date FROM Hash WHERE UserID={userid}')
                result = cur.fetchone()
                con.commit()
                cur.close()  

        #we are now checking whether or not they have changed their booking date because if they have we need to:
        # a) Check for any existing bookings that can clash whilst excluding the current booking they have
        # b) Change the digest and update it
        if ((time != result[0] or date != result[1]) and (Clashed.clashed(time, date) or time =='' or date =='')):
            return jsonify({"message": f"Unfortunately this booking is unavailable. Please re-book for another time/date.'"})
        else:            
            #retrieving data from the edit nikah_form
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]               
            email = request.form["email"]                
            phone_number = request.form["phone_number"]
            date_of_birth = request.form["date_of_birth"]               
            child_fname = request.form["child_fname"]
            child_lname = request.form["child_lname"]
            child_date_of_birth = request.form["child_date_of_birth"]

  
            data = {'First Name':first_name, 'Last Name': last_name, 'Child First Name':child_fname, 'Child Last Name': child_lname, 'Child Date of Birth': child_date_of_birth,'Email':email, 'Time': time, 'Date':date}

            invalid = Validation.validate(data= data)
            if invalid:
                return jsonify({"message": f"{invalid}"}) #error message if they did not

            #updating the digest since their time/date has changed
            if (time != result[0]) or (date != result[1]):
                hashvalue = Hash(time = time, date = date, userid = userid)
                newdigest = hashvalue.hash_algorithm()     
                updatehash = Hash(time = time, date=date, userid = userid)
                updatehash.update(newdigest= newdigest)       
                                    
                #sending them a new booking link
                user_email = Email(email= email, number= newdigest)
                user_email.send_summary_email(service = 'nikah')

                new_user = User(first_name = first_name, last_name= last_name, email = email, phone_number= phone_number, date_of_birth= date_of_birth )
                new_user.update(userid= userid)

                #updating the booking by sending it to the class Madrasah
                new_madrasah = Madrasah(user_id= userid, time= time, date= date, child_fname = child_fname , child_lname = child_lname ,child_date_of_birth= child_date_of_birth )
                new_madrasah.update()  

                return jsonify(redirect_url=url_for('routes.booking', service='nikah', digest=f'{newdigest}'))
            else:
                new_user = User(first_name = first_name, last_name= last_name, email = email, phone_number= phone_number, date_of_birth= date_of_birth )
                new_user.update(userid= userid) 

                new_madrasah = Madrasah(user_id= userid, time= time, date= date, child_fname = child_fname , child_lname = child_lname ,child_date_of_birth= child_date_of_birth )
                new_madrasah.update()  

                with sqlite3.connect('database.db') as con:
                        cur = con.cursor()
                        cur.execute(f'SELECT Digest FROM Hash WHERE UserID={userid}')
                        result = cur.fetchone()
                        digest = result[0]
                        con.commit()
                        cur.close()  

                return jsonify(redirect_url=url_for('routes.booking', service='madrasah', digest=f'{digest}'))


    else:
        return redirect(url_for('routes.madrasah_booking'))

####################  Entire Tours Process ####################



#Route to the Tours Form
@bp.route("/tourbooking")
def tours_booking():
    form_id = "TourForm"
    action_url = url_for('routes.addtour')
    service = "tour"
    return render_template("forms/tours_form.html", form_id=form_id, action_url=action_url, service = service)

#Process for Tours Table which retrieves the user input from the madrasah_form
@bp.route("/process-tour", methods=['GET','POST'])
def addtour():
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
                session.pop('random_number', None)
                return jsonify({"message": f"Unfortunately this was not the correct code. Please try again!"})
            else:
                session.pop('random_number', None)
            
            #retrieving data from the madrasah_form             
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]               
            email = request.form["email"]                
            phone_number = request.form["phone_number"]
            date_of_birth = request.form["date_of_birth"]               
            number_of_people = request.form["number_of_people"]


            # print statement for the entire form
            # print(f'Madrasahn\nverificationcode: {verification_code}\nfirst: {first_name}\nsecond: {last_name}\nemail: {email}\nphone: {phone_number}\ndob: {date_of_birth}\nchild:{child_fname}\nchildl: {child_lname}\nchilddob: {child_date_of_birth}')

            #calling the class User and storing the data for the User Table

            data = {'First Name':first_name, 'Last Name': last_name, 'Number Of People':number_of_people, 'Email':email,'Time': time, 'Date':date}

            invalid = Validation.validate(data = data)
            if invalid:
                return jsonify({"message": f"{invalid}"}) #error message if they did not

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
            new_tour = Tours(user_id= userid, time= time, date= date,number_of_people=number_of_people)
            new_tour.add_Tour()  
            
            #calculating the digest from the hash values. We are sending this to the class Hash, and receiving the digest in return.            
            hashvalue = Hash(time = time, date = date, userid = userid)
            digest = hashvalue.hash_algorithm()
            digest = hashvalue.add_digest(digest)

            #sending the summary email after inserting all data to database    
            user_email = Email(email= email, number=(digest))
            user_email.send_summary_email(service='tour')
            
            return jsonify({"message": f"Booking was successful, please check your email inbox for summary email! Feel free to make another booking as well!'"})
    else:
        return redirect(url_for('routes.tours_booking'))    


@bp.route("/edittourbooking", methods=['POST','GET'])
def edittourbooking():
    if request.method == 'POST':
        time = request.form["time"] 
        date = request.form["date"]
        userid = request.form["UserID"]
    
        with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(f'SELECT Time,Date FROM Hash WHERE UserID={userid}')
                result = cur.fetchone()
                con.commit()
                cur.close()  

        #we are now checking whether or not they have changed their booking date because if they have we need to:
        # a) Check for any existing bookings that can clash whilst excluding the current booking they have
        # b) Change the digest and update it
        if ((time != result[0] or date != result[1]) and (Clashed.clashed(time, date) or time =='' or date =='')):
            return jsonify({"message": f"Unfortunately this booking is unavailable. Please re-book for another time/date.'"})
        else:            
            #retrieving data from the edit nikah_form
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]               
            email = request.form["email"]                
            phone_number = request.form["phone_number"]
            date_of_birth = request.form["date_of_birth"]               
            number_of_people = request.form["number_of_people"]

  
            data = {'First Name':first_name, 'Last Name': last_name, 'Number Of People':number_of_people, 'Email':email,'Time': time, 'Date':date}

            invalid = Validation.validate(data= data)
            if invalid:
                return jsonify({"message": f"{invalid}"}) #error message if they did not

            #updating the digest since their time/date has changed
            if (time != result[0]) or (date != result[1]):
                hashvalue = Hash(time = time, date = date, userid = userid)
                newdigest = hashvalue.hash_algorithm()     
                updatehash = Hash(time = time, date=date, userid = userid)
                updatehash.update(newdigest= newdigest)       
                                    
                #sending them a new booking link
                user_email = Email(email= email, number= newdigest)
                user_email.send_summary_email(service = 'tour')

                new_user = User(first_name = first_name, last_name= last_name, email = email, phone_number= phone_number, date_of_birth= date_of_birth )
                new_user.update(userid= userid)

                #updating the booking by sending it to the class Madrasah
                new_tour = Tours(user_id= userid, time= time, date= date, number_of_people=number_of_people )
                new_tour.update()  

                return jsonify(redirect_url=url_for('routes.booking', service='tour', digest=f'{newdigest}'))
            else:
                new_user = User(first_name = first_name, last_name= last_name, email = email, phone_number= phone_number, date_of_birth= date_of_birth )
                new_user.update(userid= userid) 

                new_tour = Tours(user_id= userid, time= time, date= date, number_of_people=number_of_people )
                new_tour.update()  

                with sqlite3.connect('database.db') as con:
                        cur = con.cursor()
                        cur.execute(f'SELECT Digest FROM Hash WHERE UserID={userid}')
                        result = cur.fetchone()
                        digest = result[0]
                        con.commit()
                        cur.close()  

                return jsonify(redirect_url=url_for('routes.booking', service='tour', digest=f'{digest}'))


    else:
        return redirect(url_for('routes.tours_booking'))





####################  Entire Booking/Editing Process ####################
@bp.route('/booking/<service>/<digest>')
def booking(service, digest):
    if service == 'nikah':
        #inserting the data into the table for the user to see. We find the user's data through the digest
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(f"SELECT * FROM User JOIN Nikah ON User.UserID = Nikah.UserID JOIN Hash ON User.UserID = Hash.UserID WHERE Hash.Digest= '{digest}'")
        rows = cur.fetchall()
        con.close()
        #if the digest never existed we return the error page
        if len(rows) == 0:
            return'OH NO YOU DONT HAVE A BOOKING L'
        return render_template("tables/nikah_table.html", rows = rows) 

    elif service == 'madrasah':
        #inserting the data into the table for the user to see. We find the user's data through the digest
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(f"SELECT * FROM User JOIN Madrasah ON User.UserID = Madrasah.UserID JOIN Hash ON User.UserID = Hash.UserID WHERE Hash.Digest= '{digest}'")
        rows = cur.fetchall()
        con.close()
        #if the digest never existed we return the error page
        if len(rows) == 0:
            return'OH NO YOU DONT HAVE A BOOKING L'
        return render_template("tables/madrasah_table.html", rows = rows)       


    elif service == 'tour':
        #inserting the data into the table for the user to see. We find the user's data through the digest
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(f"SELECT * FROM User JOIN Tours ON User.UserID = Tours.UserID JOIN Hash ON User.UserID = Hash.UserID WHERE Hash.Digest= '{digest}'")
        rows = cur.fetchall()
        con.close()
        #if the digest never existed we return the error page
        if len(rows) == 0:
            return'OH NO YOU DONT HAVE A BOOKING L'
        return render_template("tables/tour_table.html", rows = rows)          


@bp.route("/edit/<service>", methods=['POST','GET'])
def edit(service):
    if (request.method == 'POST' and service=='nikah'):
        #this is the edit form. We are inserting the current data into the form and will now allow the user to edit it.
        try:
            userid = request.form['userid']
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
        
    elif (request.method == 'POST' and service=='madrasah'):
        try:
            userid = request.form['userid']
            connection = sqlite3.connect("database.db")
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM User u JOIN Madrasah t ON u.UserID = t.UserID WHERE u.UserID={userid}")
            rows = cursor.fetchall()
        except:
            userid=None
        finally:
            connection.close()
            return render_template("forms/edit_forms/editmadrasah.html",rows=rows)

    elif (request.method == 'POST' and service=='tour'):
        try:
            userid = request.form['userid']
            connection = sqlite3.connect("database.db")
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM User u JOIN Tours t ON u.UserID = t.UserID WHERE u.UserID={userid}")
            rows = cursor.fetchall()
        except:
            userid=None
        finally:
            connection.close()
            return render_template("forms/edit_forms/edittour.html",rows=rows)          










###### DELETING THE BOOKING #####





@bp.route("/delete/<service>", methods=['POST','GET'])
def delete(service):
    if (request.method == 'POST' and service =='nikah'):
        try:
            userid = request.form['userid']
            deletebooking = Nikah.delete(userid=userid)
            return(f'{deletebooking}')
        except:
            msg = 'error in smth with deletion'
            return render_template("pages/nikah.html")
    
    elif (request.method == 'POST' and service =='madrasah'):
        try:
            userid = request.form['userid']
            deletebooking = Madrasah.delete(userid=userid)
            return(f'{deletebooking}')
        except:
            msg = 'error in smth with deletion'
            return render_template("pages/madrasah.html")        



###basically after adding the json what now happens is that in the Nikah form all the required fields do not work HOWEVER the madrasah fields still work. Weird thing fr. we will need to debug this dumb thing and see why it happens


##IDEA TO REDIRECT THE USER BACK TO THE TABLE PAEG AFTER THEY  EDIT 




