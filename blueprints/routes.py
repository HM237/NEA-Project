from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from models import User, Nikah, Madrasah,Tours,Functions,Payment, Clashed, Email, Hash, Validation, DatabaseError, ServerError, UnboundLocalErrors, SocketError
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


#Route to the Service Page
@bp.route('/errors/<errormsg>')
def errors(errormsg):
    msg = f'The error that you ran into was: {errormsg}'
    return render_template("pages/error.html", errormsg = msg)







####################  Entire Verification Process ####################

#Route to the verification process. Uses a dynamic URL to identify which service is using the verification process.
@bp.route("/verification/<service>", methods = ['GET','POST'])
def verification(service):
    #here we are generating a random 6 digit number which will act as our verification code. We then use Flask session to store this number for this session. This will allow me to compare the verification-code later on, to determine if the code is correct or incorrect.
    random_number = random.randint(111111,999999)
    print(f'Verification Code: {random_number}')
    session['random_number'] = random_number
    try:
        if request.method == 'POST':
            email = request.form.get('email')
            match = re.match(r"""^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$""", email) #this regular expression is used to identify if the email is in a valid format.
            if not match:
                session.pop('random_number', None) #if the email is invalid, we will pop the verification code stored in Flask session and prompt the user to enter a valid email.
                return jsonify({"message": f"PLease enter a valid email before trying to send a verification code."})

            time = request.form.get('time')
            date = request.form.get('date')
            #this if statement checks if the booking will clash with another booking.
            if Clashed.clashed(time, date) or (time == '') or (date==''):
                return jsonify({"message": f"Unfortunately this booking is unavailable. Please re-book for another time/date.'"}) #User is prompted to choose another booking if the booking has already been taken.
            
            if service == 'nikah':
                #the first part of the if statement validates the user-input for the service nikah.
                first_name = request.form["first_name"]
                last_name = request.form["last_name"]
                groom_first_name = request.form["groom_first_name"]               
                groom_last_name = request.form["groom_last_name"]               
                bride_first_name = request.form["bride_first_name"]               
                bride_last_name = request.form["bride_last_name"]               
                email = request.form["email"]                            
                post_code = request.form["post_code"]            
                address_line = request.form["address_line"]              

                #below we are storing the data in a dictionary to pass on to the Validation Class.
                data = {'First Name': first_name, 
                        'Last Name': last_name, 
                        'Groom First Name':groom_first_name, 
                        'Groom Last Name': groom_last_name, 
                        'Bride First Name': bride_first_name, 
                        'Bride Last Name': bride_last_name,
                        'Email':email ,
                        'Address Line':address_line, 
                        'Post Code':post_code, 
                        'Time':time, 
                        'Date': date}
                
                invalid = Validation.validate(data= data) # The Validation Class returns a bool whether True or False.
                if invalid:

                    return jsonify({"message": f"{invalid}"}) #If Invalid = True, that means one of the user-input was invalid, and so we prompt the user enter a valid input.
                else:
                    
                    try:
                        #if invalid = False, we can send the Verification Email to the user 
                        user_email = Email(email= email, number = random_number)
                        user_email.send_verification_email()
                        return jsonify({"message": f"Verification email sent successfully, please check your email inbox!'"}) #notifies the user to check their inbox     
                    
                    except UnboundLocalErrors:
                        return jsonify({"message": f"A value could not be attributed. Please try again later."}) 
                    
                    except SocketError:
                        return jsonify({"message": f"Unfortunately the form could not send the verification email. Please try again later."}) 

                    except ServerError:
                        return jsonify({"message": f"Unfortunately the server could not connect. Please check that you are connected to the Internet or try again later."})                
                    except Exception:
                        return jsonify({"message": f"An unexpected error has occurred. Please contact the masjid and report this error."}) 
                        
            elif service =='madrasah':
                #the first part of the if statement validates the user-input for the service madrasah.
                first_name = request.form["first_name"]
                last_name = request.form["last_name"]               
                email = request.form["email"]                
                child_fname = request.form["child_fname"]
                child_lname = request.form["child_lname"]
                child_date_of_birth = request.form["child_date_of_birth"]

                #below we are storing the data in a dictionary to pass on to the Validation Class.
                data = {'First Name':first_name, 
                        'Last Name': last_name, 
                        'Child First Name':child_fname, 
                        'Child Last Name': child_lname, 
                        'Child Date of Birth': child_date_of_birth, 
                        'Email':email,
                        'Time': time, 
                        'Date':date}

                invalid = Validation.validate(data = data)
                if invalid:

                    return jsonify({"message": f"{invalid}"}) #If Invalid = True, that means one of the user-input was invalid, and so we prompt the user enter a valid input.
                else:
                    
                    try:
                        #if invalid = False, we can send the Verification Email to the user 
                        user_email = Email(email= email, number = random_number)
                        user_email.send_verification_email()
                        return jsonify({"message": f"Verification email sent successfully, please check your email inbox!'"}) #notifies the user to check their inbox     
                    
                    except UnboundLocalErrors:
                        return jsonify({"message": f"A value could not be attributed. Please try again later."}) 
                    
                    except SocketError:
                        return jsonify({"message": f"Unfortunately the form could not send the verification email. Please try again later."}) 

                    except ServerError:
                        return jsonify({"message": f"Unfortunately the server could not connect. Please check that you are connected to the Internet or try again later."})                
                    except Exception:
                        return jsonify({"message": f"An unexpected error has occurred. Please contact the masjid and report this error."})      


            elif service == 'tour':
                first_name = request.form["first_name"]
                last_name = request.form["last_name"]      
                email = request.form["email"]      
                post_code = request.form["post_code"]            
                address_line = request.form["address_line"]  
                number_of_people = request.form["number_of_people"]  

                #below we are storing the data in a dictionary to pass on to the Validation Class.

                data = {'First Name': first_name, 
                        'Last Name': last_name,
                        'Email':email,
                        'Address Line':address_line, 
                        'Post Code':post_code, 
                        'Number of People':number_of_people,
                        'Time':time, 
                        'Date': date}
                
                invalid = Validation.validate(data= data)
                if invalid:
                    return jsonify({"message": f"{invalid}"})#If Invalid = True, that means one of the user-input was invalid, and so we prompt the user enter a valid input.
                else:
                    #if invalid = False, we can send the Verification Email to the user 
                    try:
                        user_email = Email(email= email, number = random_number)
                        user_email.send_verification_email()
                        return jsonify({"message": f"Verification email sent successfully, please check your email inbox!'"})#notifies the user to check their inbox
                                    
                    except UnboundLocalErrors:
                        return jsonify({"message": f"A value could not be attributed. Please try again later."}) 
                    
                    except SocketError:
                        return jsonify({"message": f"Unfortunately the form could not send the verification email. Please try again later."}) 

                    except ServerError:
                        return jsonify({"message": f"Unfortunately the server could not connect. Please check that you are connected to the Internet or try again later."})                
                    
                    except Exception:
                        return jsonify({"message": f"An unexpected error has occurred. Please contact the masjid and report this error."}) 

            elif service == 'function':
                first_name = request.form["first_name"]
                last_name = request.form["last_name"]               
                email = request.form["email"]        
                post_code = request.form["post_code"]            
                address_line = request.form["address_line"]     

                #below we are storing the data in a dictionary to pass on to the Validation Class.
                data = {'First Name':first_name, 
                        'Last Name': last_name, 
                        'Address Line':address_line, 
                        'Post Code':post_code, 
                        'Email':email,
                        'Time': time, 
                        'Date':date}
                
                invalid = Validation.validate(data = data)
                if invalid:
                    return jsonify({"message": f"{invalid}"}) #If Invalid = True, that means one of the user-input was invalid, and so we prompt the user enter a valid input.  
                else:
                    try:
                        #if invalid = False, we can send the Verification Email to the user 
                        user_email = Email(email= email, number = random_number)
                        user_email.send_verification_email()
                        return jsonify({"message": f"Verification email sent successfully, please check your email inbox!'"}) #notifies the user to check their inbox     
                    
                    except UnboundLocalErrors:
                        return jsonify({"message": f"A value could not be attributed. Please try again later."}) 
                    
                    except SocketError:
                        return jsonify({"message": f"Unfortunately the form could not send the verification email. Please try again later."}) 

                    except ServerError:
                        return jsonify({"message": f"Unfortunately the server could not connect. Please check that you are connected to the Internet or try again later."})                
                    
                    except Exception:
                        return jsonify({"message": f"An unexpected error has occurred. Please contact the masjid and report this error."}) 

            else:
                return jsonify(redirect_url=url_for('routes.errors', errormsg = f'Invalid'))
    except Exception as e:
        return jsonify(redirect_url=url_for('routes.errors', errormsg = f'{e}'))

    return jsonify(redirect_url=url_for('routes.index'))










####################  Entire Nikah Process ####################

# Route to the Nikah Form 
@bp.route("/nikahbooking")
def nikah_booking():
    #Filling in the formId, actionURL and service for the nikah form.
    form_id = "NikahForm"
    action_url = url_for('routes.addnikah')
    service = "nikah"
    return render_template("forms/nikah_form.html", form_id=form_id, action_url=action_url, service = service )


#Process for Nikah Table which retrieves the input from the nikah_form.
@bp.route("/process-nikah", methods=['GET','POST'])
def addnikah():
    random_number = session.get('random_number') # Retrieves the stored random number in our Flask session.
    if random_number: #if the session has no value, we will prompt the user to press the 'Send Verification'  button.
        print(f'The verification code was generated: {random_number}')
    else:
        return jsonify({"message": f"Please press the 'Send Verifcation' button to send the code to your box first!"})
    try:
        if request.method == 'POST':        
            time = request.form["time"] 
            date = request.form["date"]
            #Re-checks if the user has tried to make a booking that has already been made.
            if Clashed.clashed(time, date):
                return jsonify({"message": f"Unfortunately this booking is unavailable. Please re-book for another time/date.'"})
            else:
                #now verifying if the user submiited the right verification code
                verification_code = request.form["verification-code"]
                if (not verification_code.isnumeric()) or (int(verification_code) != random_number):
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

                #rechecking if the user inputs are valid
                data = {'First Name': first_name, 
                        'Last Name': last_name, 
                        'Groom First Name':groom_first_name, 
                        'Groom Last Name': groom_last_name, 
                        'Bride First Name': bride_first_name, 
                        'Bride Last Name': bride_last_name,
                        'Email':email ,
                        'Address Line':address_line,
                        'Post Code':post_code, 
                        'Time':time, 
                        'Date': date}
                        
                invalid = Validation.validate(data= data)
                if invalid:
                    return jsonify({"message": f"{invalid}"}) #error message if they did not

                try:
                    #User Class is used to store the data for the User Table
                    new_user = User(first_name = first_name, last_name= last_name, email = email, phone_number= phone_number, date_of_birth= date_of_birth )
                    new_user.add_User()
                    #retrieving the latest userid to store the other data
                    with sqlite3.connect('database.db') as con:
                            cur = con.cursor()
                            cur.execute('SELECT seq FROM sqlite_sequence WHERE name="User"')
                            result = cur.fetchone()
                            userid = result[0]
                            con.commit()
                            cur.close()
                    
                    #Nikah Class used to store the data for the Nikah Table
                    new_nikah = Nikah(user_id= userid,groom_first_name= groom_first_name , groom_last_name= groom_last_name , bride_first_name=bride_first_name , bride_last_name=bride_last_name , post_code= post_code, address_line= address_line)
                    new_nikah.add_Nikah()  
                    
                    #Payment Class used to store the data for the Payment Table
                    new_payment = Payment(user_id= userid, post_code= post_code, address_line= address_line, payment_method= payment_method, price = price)
                    new_payment.add_Payment()

                    #calculating the digest from the hash values. We are sending this to the Hash Class, and receiving the digest in return.
                    hashvalue = Hash(time = time, date = date, userid = userid)
                    digest = hashvalue.hash_algorithm()
                    digest = hashvalue.add_digest(digest) #Adding the digest to the Hash Table

                except sqlite3.OperationalError:
                        return jsonify({"message": f"The database is currently locked. Please try again later. If the issue still persists, please inform the masjid."})  

                except sqlite3.DatabaseError:
                    return jsonify({"message": f"An unexpected error has occured with the database. Please try again later. If the issue still persists, please inform the masjid."})                               
                
                except Exception as e:
                    return jsonify({"message": f"This error: {e} has occured. Please try again later to submit this booking or inform the masjid."})                     

                try:
                    #sending the summary email after inserting all data to database. 
                    user_email = Email(email= email, number=(digest))
                    user_email.send_summary_email(service='nikah') #Fills in the dynamic URL for the booking URL.
                    return jsonify({"message": f"Booking was successful, please check your email inbox for summary email!!'"}) #notifies the user that the booking was a success    
                
                except UnboundLocalErrors:
                    return jsonify({"message": f"A value could not be attributed. Please try again later."}) 
                
                except SocketError:
                    return jsonify({"message": f"Unfortunately the form could not send the summary email. Please try again later."}) 

                except ServerError:
                    return jsonify({"message": f"Unfortunately the server could not connect. Please check that you are connected to the Internet or try again later."})                
                except Exception:
                    return jsonify({"message": f"An unexpected error has occurred. Please contact the masjid and report this error."})                 

    except Exception as e:
        return jsonify(redirect_url=url_for('routes.errors', errormsg = f'{e}'))
    
    return jsonify(redirect_url=url_for('routes.nikah'))




@bp.route("/editnikahbooking", methods=['POST','GET'])
def editnikahbooking():
    try:
        if request.method == 'POST':
            time = request.form["time"] 
            date = request.form["date"]
            userid = request.form["UserID"]
        
            try:
                #retrieving the current time and date of the User
                with sqlite3.connect('database.db') as con:
                        cur = con.cursor()
                        cur.execute(f'SELECT Time,Date FROM Hash WHERE UserID={userid}')
                        result = cur.fetchone()
                        con.commit()
                        cur.close()          
            except Exception as e:
                        return jsonify({"message": f"This error: {e} has occured. Please try again later to delete this booking or inform the masjid."})     
            #we are now checking whether or not they have changed their booking time/date because if they have we need to:
            # a) Check for any existing bookings that can clash whilst excluding the current booking they have
            # b) Update the digest 
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

                #validating the user inputs by sending the data in a dictionary to the Validation Class.
                data = {'First Name': first_name, 
                        'Last Name': last_name, 
                        'Groom First Name':groom_first_name, 
                        'Groom Last Name': groom_last_name, 
                        'Bride First Name': bride_first_name, 
                        'Bride Last Name': bride_last_name, 
                        'Email':email,
                        'Address Line':address_line, 
                        'Post Code':post_code, 
                        'Time':time, 
                        'Date': date}


                invalid = Validation.validate(data= data)
                if invalid:
                    return jsonify({"message": f"{invalid}"}) #return the fields that need a valid input.

                #updating the digest if their booking time/date has changed
                if (time != result[0]) or (date != result[1]):
                    hashvalue = Hash(time = time, date = date, userid = userid)
                    newdigest = hashvalue.hash_algorithm()     
                    updatehash = Hash(time = time, date=date, userid = userid)
                    updatehash.update(newdigest= newdigest)       
                                        
                    try:                                    
                        #sending them a new booking link
                        user_email = Email(email= email, number= newdigest)
                        user_email.send_summary_email(service = 'nikah')
                        
                    except UnboundLocalErrors:
                        return jsonify({"message": f"A value could not be attributed. Please try again later."}) 
                    
                    except SocketError:
                        return jsonify({"message": f"Unfortunately the form could not send the summary email. Please try again later."}) 

                    except ServerError:
                        return jsonify({"message": f"Unfortunately the server could not connect. Please check that you are connected to the Internet or try again later."})                
                    except Exception:
                        return jsonify({"message": f"An unexpected error has occurred. Please contact the masjid and report this error."})                      

                    try:
                        new_user = User(first_name = first_name, last_name= last_name, email = email, phone_number= phone_number, date_of_birth= date_of_birth )
                        new_user.update(userid= userid)

                        #updating the booking by sending it to the Nikah Class
                        new_nikah = Nikah(groom_first_name = groom_first_name, groom_last_name= groom_last_name , bride_first_name=bride_first_name , bride_last_name=bride_last_name ,post_code= post_code, address_line= address_line, user_id=userid)
                        new_nikah.update()  

                        return jsonify(redirect_url=url_for('routes.booking', service='nikah', digest=f'{newdigest}')) #Rerouting the user to the new editing/viewing page with the new digest.

                    except sqlite3.OperationalError:
                            return jsonify({"message": f"The database is currently locked. Please try again later. If the issue still persists, please inform the masjid."})  

                    except sqlite3.DatabaseError:
                        return jsonify({"message": f"An unexpected error has occured with the database. Please try again later. If the issue still persists, please inform the masjid."})                               
                    
                    except Exception as e:
                        return jsonify({"message": f"This error: {e} has occured. Please try again later to delete this booking or inform the masjid."})                         
                else:

                    try:
                        #if they haven't changed their booking time/date we can reroute them to their current editing/viewing page after updating the data in the User and Nikah Table.
                        new_user = User(first_name = first_name, last_name= last_name, email = email, phone_number= phone_number, date_of_birth= date_of_birth )
                        new_user.update(userid= userid) 

                        new_nikah = Nikah(groom_first_name= groom_first_name , 
                                        groom_last_name= groom_last_name , 
                                        bride_first_name=bride_first_name , 
                                        bride_last_name=bride_last_name , 
                                        post_code= post_code, 
                                        address_line= address_line, 
                                        user_id=userid)
                        
                        new_nikah.update()  

                        with sqlite3.connect('database.db') as con:
                                cur = con.cursor()
                                cur.execute(f'SELECT Digest FROM Hash WHERE UserID={userid}')
                                result = cur.fetchone()
                                digest = result[0]
                                con.commit()
                                cur.close()  

                        return jsonify(redirect_url=url_for('routes.booking', service='nikah', digest=f'{digest}'))

                    except sqlite3.OperationalError:
                            return jsonify({"message": f"The database is currently locked. Please try again later. If the issue still persists, please inform the masjid."})  

                    except sqlite3.DatabaseError:
                        return jsonify({"message": f"An unexpected error has occured with the database. Please try again later. If the issue still persists, please inform the masjid."})                               
                    
                    except Exception as e:
                        return jsonify({"message": f"This error: {e} has occured. Please try again later to delete this booking or inform the masjid."})     

    except Exception as e:
        return jsonify(redirect_url=url_for('routes.errors', errormsg = f'{e}'))
    
    return jsonify(redirect_url=url_for('routes.nikah'))










####################  Entire Madrasah Process ####################

#Route to the Madrasah Form
@bp.route("/madrasahbooking")
def madrasah_booking():
    #Filling in the formId, actionURL and service for the madrasah form.
    form_id = "MadrasahForm"
    action_url = url_for('routes.addmadrasah')
    service = "madrasah"
    return render_template("forms/madrasah_form.html", form_id=form_id, action_url=action_url, service = service)

#Process for Madrasah Table which retrieves the user input from the madrasah_form
@bp.route("/process-madrasah", methods=['GET','POST'])
def addmadrasah():
    #same steps that were explain on line 196 just changed for the Madrasah Process.
    random_number = session.get('random_number') 
    if random_number:
        print(f'The verification code generated: {random_number}')
    else:
        return jsonify({"message": f"Please press the 'Send Verifcation' button to send the code to your box first!"})    
    try:
        if request.method == 'POST':        
            time = request.form["time"]
            date = request.form["date"]
            #checking for any bookings that could clash
            if Clashed.clashed(time, date):
                return jsonify({"message": f"Unfortunately this booking is unavailable. Please re-book for another time/date.'"})
            
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



                #User Class stores the data in the User Table

                data = {'First Name':first_name, 
                        'Last Name': last_name, 
                        'Child First Name':child_fname, 
                        'Child Last Name': child_lname, 
                        'Child Date of Birth': child_date_of_birth, 
                        'Email':email,
                        'Time': time, 
                        'Date':date}

                invalid = Validation.validate(data = data)
                if invalid:
                    return jsonify({"message": f"{invalid}"}) #error message if they did not


                try:
                    new_user = User(first_name = first_name, 
                                    last_name= last_name, 
                                    email = email, 
                                    phone_number= phone_number, 
                                    date_of_birth= date_of_birth)
                    
                    new_user.add_User()
                    
                    with sqlite3.connect('database.db') as con:
                            cur = con.cursor()
                            cur.execute('SELECT seq FROM sqlite_sequence WHERE name="User"')
                            result = cur.fetchone()
                            userid = result[0]
                            con.commit()
                            cur.close()
                    
                    #Masdrasah Class stores the data in the Madrasah Table
                    new_madrasah = Madrasah(user_id= userid, 
                                            child_fname = child_fname , 
                                            child_lname = child_lname ,
                                            child_date_of_birth= child_date_of_birth )
                    
                    new_madrasah.add_Madrasah()  
                    
                    #calculating the digest from the hash values. We are sending this to the Hash Class and receiving the digest in return.            
                    hashvalue = Hash(time = time, date = date, userid = userid)
                    digest = hashvalue.hash_algorithm()
                    digest = hashvalue.add_digest(digest)

                except sqlite3.OperationalError:
                        return jsonify({"message": f"The database is currently locked. Please try again later. If the issue still persists, please inform the masjid."})  

                except sqlite3.DatabaseError:
                    return jsonify({"message": f"An unexpected error has occured with the database. Please try again later. If the issue still persists, please inform the masjid."})                               
                
                except Exception as e:
                    return jsonify({"message": f"This error: {e} has occured. Please try again later to submit this booking or inform the masjid."})                     

                try:
                    #sending the summary email after inserting all data to database    
                    user_email = Email(email= email, number=(digest))
                    user_email.send_summary_email(service='madrasah')
                    return jsonify({"message": f"Booking was successful, please check your email inbox for summary email! Feel free to make another booking as well!'"})
                
                except UnboundLocalErrors:
                    return jsonify({"message": f"A value could not be attributed. Please try again later."}) 
                
                except SocketError:
                    return jsonify({"message": f"Unfortunately the form could not send the summary email. Please try again later."}) 

                except ServerError:
                    return jsonify({"message": f"Unfortunately the server could not connect. Please check that you are connected to the Internet or try again later."})                
                except Exception:
                    return jsonify({"message": f"An unexpected error has occurred. Please contact the masjid and report this error."}) 
                 
    except Exception as e:
        return jsonify(redirect_url=url_for('routes.errors', errormsg = f'{e}'))
    
    return jsonify(redirect_url=url_for('routes.madrasah_booking'))


@bp.route("/editmadrasahbooking", methods=['POST','GET'])
def editmadrasahbooking():
    try:
        if request.method == 'POST':
            time = request.form["time"] 
            date = request.form["date"]
            userid = request.form["UserID"]
        
            try:
                with sqlite3.connect('database.db') as con:
                        cur = con.cursor()
                        cur.execute(f'SELECT Time,Date FROM Hash WHERE UserID={userid}')
                        result = cur.fetchone()
                        con.commit()
                        cur.close()  
            except Exception as e:
                return jsonify({"message": f"This error: {e} has occured. Please try again later to delete this booking or inform the masjid."})                         

            #we are now checking whether or not they have changed their booking date because if they have we need to:
            # a) Check for any existing bookings that can clash whilst excluding the current booking they have.
            # b) Update the digest when an available booking is made.
            if ((time != result[0] or date != result[1]) and (Clashed.clashed(time, date) or time =='' or date =='')):
                return jsonify({"message": f"Unfortunately this booking is unavailable. Please re-book for another time/date.'"})
            else:            
                #retrieving data from the edit madrasah_form
                first_name = request.form["first_name"]
                last_name = request.form["last_name"]               
                email = request.form["email"]                
                phone_number = request.form["phone_number"]
                date_of_birth = request.form["date_of_birth"]               
                child_fname = request.form["child_fname"]
                child_lname = request.form["child_lname"]
                child_date_of_birth = request.form["child_date_of_birth"]

    
                data = {'First Name':first_name, 
                        'Last Name': last_name, 
                        'Child First Name':child_fname, 
                        'Child Last Name': child_lname, 
                        'Child Date of Birth': child_date_of_birth,
                        'Email':email, 
                        'Time': time, 
                        'Date':date}

                invalid = Validation.validate(data= data)
                if invalid:
                    return jsonify({"message": f"{invalid}"}) #error message if they did not

                #updating the digest since their time/date has changed
                if (time != result[0]) or (date != result[1]):
                    hashvalue = Hash(time = time, date = date, userid = userid)
                    newdigest = hashvalue.hash_algorithm()     
                    updatehash = Hash(time = time, date=date, userid = userid)
                    updatehash.update(newdigest= newdigest)       
                                        
                    try:                                    
                        #sending them a new booking link
                        user_email = Email(email= email, number= newdigest)
                        user_email.send_summary_email(service = 'nikah')

                    except UnboundLocalErrors:
                        return jsonify({"message": f"A value could not be attributed. Please try again later."}) 
                    
                    except SocketError:
                        return jsonify({"message": f"Unfortunately the form could not send the summary email. Please try again later."}) 

                    except ServerError:
                        return jsonify({"message": f"Unfortunately the server could not connect. Please check that you are connected to the Internet or try again later."})                
                    except Exception:
                        return jsonify({"message": f"An unexpected error has occurred. Please contact the masjid and report this error."})                      

                    try:
                        new_user = User(first_name = first_name, 
                                        last_name= last_name, 
                                        email = email, 
                                        phone_number= phone_number, 
                                        date_of_birth= date_of_birth )
                        
                        new_user.update(userid= userid)

                        #updating the booking by sending it to the Madrasah Class.
                        new_madrasah = Madrasah(user_id= userid, 
                                                child_fname = child_fname , 
                                                child_lname = child_lname ,
                                                child_date_of_birth= child_date_of_birth )
                        new_madrasah.update()  

                        return jsonify(redirect_url=url_for('routes.booking', service='nikah', digest=f'{newdigest}'))

                    except sqlite3.OperationalError:
                            return jsonify({"message": f"The database is currently locked. Please try again later. If the issue still persists, please inform the masjid."})  

                    except sqlite3.DatabaseError:
                        return jsonify({"message": f"An unexpected error has occured with the database. Please try again later. If the issue still persists, please inform the masjid."})                               
                    
                    except Exception as e:
                        return jsonify({"message": f"This error: {e} has occured. Please try again later to delete this booking or inform the masjid."})     

                else:

                    try:
                        new_user = User(first_name = first_name, 
                                        last_name= last_name, 
                                        email = email, 
                                        phone_number= phone_number, 
                                        date_of_birth= date_of_birth )
                        
                        new_user.update(userid= userid) 

                        new_madrasah = Madrasah(user_id= userid,
                                                child_fname = child_fname , 
                                                child_lname = child_lname ,
                                                child_date_of_birth= child_date_of_birth )
                        
                        new_madrasah.update()  

                        with sqlite3.connect('database.db') as con:
                                cur = con.cursor()
                                cur.execute(f'SELECT Digest FROM Hash WHERE UserID={userid}')
                                result = cur.fetchone()
                                digest = result[0]
                                con.commit()
                                cur.close()  

                        return jsonify(redirect_url=url_for('routes.booking', service='madrasah', digest=f'{digest}'))

                    except sqlite3.OperationalError:
                            return jsonify({"message": f"The database is currently locked. Please try again later. If the issue still persists, please inform the masjid."})  

                    except sqlite3.DatabaseError:
                        return jsonify({"message": f"An unexpected error has occured with the database. Please try again later. If the issue still persists, please inform the masjid."})                               
                    
                    except Exception as e:
                        return jsonify({"message": f"This error: {e} has occured. Please try again later to delete this booking or inform the masjid."})                         


    except Exception as e:
        return jsonify(redirect_url=url_for('routes.errors', errormsg = f'{e}'))
    
    return jsonify(redirect_url=url_for('routes.madrasah_booking'))










####################  Entire Tours Process ####################

#Route to the Tours Form
@bp.route("/tourbooking")
def tours_booking():
    form_id = "TourForm"
    action_url = url_for('routes.addtour')
    service = "tour"
    return render_template("forms/tours_form.html", form_id=form_id, action_url=action_url, service = service)

#Process for Tours Table which retrieves the user input from the tour_form
@bp.route("/process-tour", methods=['GET','POST'])
def addtour():
    #same comments as line 192
    random_number = session.get('random_number') # Retrieve and remove the stored random number
    if random_number:
        print(f'The verification code generated: {random_number}')
    else:
        return jsonify({"message": f"Please press the 'Send Verifcation' button to send the code to your box first!"})    
    try:
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
                
                #retrieving data from the tour_form             
                first_name = request.form["first_name"]
                last_name = request.form["last_name"]               
                email = request.form["email"]                
                phone_number = request.form["phone_number"]
                date_of_birth = request.form["date_of_birth"]               
                number_of_people = request.form["number_of_people"]

                #calling the User Class and storing the data in the User Table

                data = {'First Name':first_name, 
                        'Last Name': last_name, 
                        'Number Of People':number_of_people, 
                        'Email':email,
                        'Time': time, 
                        'Date':date}

                invalid = Validation.validate(data = data)
                if invalid:
                    return jsonify({"message": f"{invalid}"}) #error message if they did not


                try:
                    new_user = User(first_name = first_name, 
                                    last_name= last_name, 
                                    email = email, 
                                    phone_number= phone_number, 
                                    date_of_birth= date_of_birth)
                    
                    new_user.add_User()
                    
                    with sqlite3.connect('database.db') as con:
                            cur = con.cursor()
                            cur.execute('SELECT seq FROM sqlite_sequence WHERE name="User"')
                            result = cur.fetchone()
                            userid = result[0]
                            con.commit()
                            cur.close()
                    
                    #Tour Class stores the data in the Tour Table.
                    new_tour = Tours(user_id= userid, number_of_people=number_of_people)
                    new_tour.add_Tour()  
                    
                
                    #calculating the digest from the hash values. We are sending this to the Hash Class, and receiving the digest in return.            
                    hashvalue = Hash(time = time, date = date, userid = userid)
                    digest = hashvalue.hash_algorithm()
                    digest = hashvalue.add_digest(digest)

                except sqlite3.OperationalError:
                        return jsonify({"message": f"The database is currently locked. Please try again later. If the issue still persists, please inform the masjid."})  

                except sqlite3.DatabaseError:
                    return jsonify({"message": f"An unexpected error has occured with the database. Please try again later. If the issue still persists, please inform the masjid."})                               
                
                except Exception as e:
                    return jsonify({"message": f"This error: {e} has occured. Please try again later to submit this booking or inform the masjid."})     


                try:
                    #sending the summary email after inserting all data to database    
                    user_email = Email(email= email, number=(digest))
                    user_email.send_summary_email(service='tour')
                    return jsonify({"message": f"Booking was successful, please check your email inbox for summary email! Feel free to make another booking as well!'"})

                except UnboundLocalErrors:
                    return jsonify({"message": f"A value could not be attributed. Please try again later."}) 
                
                except SocketError:
                    return jsonify({"message": f"Unfortunately the form could not send the summary email. Please try again later."}) 

                except ServerError:
                    return jsonify({"message": f"Unfortunately the server could not connect. Please check that you are connected to the Internet or try again later."})                
                except Exception:
                    return jsonify({"message": f"An unexpected error has occurred. Please contact the masjid and report this error."})                      
            

    except Exception as e:
        return jsonify(redirect_url=url_for('routes.errors', errormsg = f'{e}'))
    
    return jsonify(redirect_url=url_for('routes.tours_booking'))


@bp.route("/edittourbooking", methods=['POST','GET'])
def edittourbooking():
    try:
        if request.method == 'POST':
            time = request.form["time"] 
            date = request.form["date"]
            userid = request.form["UserID"]
        
            try:
                with sqlite3.connect('database.db') as con:
                        cur = con.cursor()
                        cur.execute(f'SELECT Time,Date FROM Hash WHERE UserID={userid}')
                        result = cur.fetchone()
                        con.commit()
                        cur.close()  
            except Exception as e:
                return jsonify({"message": f"This error: {e} has occured. Please try again later to delete this booking or inform the masjid."})                         

            #we are now checking whether or not they have changed their booking date because if they have we need to:
            # a) Check for any existing bookings that can clash whilst excluding the current booking they have
            # b) Update the digest.
            if ((time != result[0] or date != result[1]) and (Clashed.clashed(time, date) or time =='' or date =='')):
                return jsonify({"message": f"Unfortunately this booking is unavailable. Please re-book for another time/date.'"})
            else:            
                #retrieving data from the edittour form.
                first_name = request.form["first_name"]
                last_name = request.form["last_name"]               
                email = request.form["email"]                
                phone_number = request.form["phone_number"]
                date_of_birth = request.form["date_of_birth"]               
                number_of_people = request.form["number_of_people"]

    
                data = {'First Name':first_name, 
                        'Last Name': last_name, 
                        'Number Of People':number_of_people, 
                        'Email':email,
                        'Time': time, 
                        'Date':date}

                invalid = Validation.validate(data= data)
                if invalid:
                    return jsonify({"message": f"{invalid}"}) 

                #updating the digest since their time/date has changed
                if (time != result[0]) or (date != result[1]):
                    hashvalue = Hash(time = time, date = date, userid = userid)
                    newdigest = hashvalue.hash_algorithm()     
                    updatehash = Hash(time = time, date=date, userid = userid)
                    updatehash.update(newdigest= newdigest)       
                                        
                    try:                                            
                        #sending them a new booking link
                        user_email = Email(email= email, number= newdigest)
                        user_email.send_summary_email(service = 'tour')

                    except UnboundLocalErrors:
                        return jsonify({"message": f"A value could not be attributed. Please try again later."}) 
                    
                    except SocketError:
                        return jsonify({"message": f"Unfortunately the form could not send the summary email. Please try again later."}) 

                    except ServerError:
                        return jsonify({"message": f"Unfortunately the server could not connect. Please check that you are connected to the Internet or try again later."})                
                    except Exception:
                        return jsonify({"message": f"An unexpected error has occurred. Please contact the masjid and report this error."})                      

                    try:
                        new_user = User(first_name = first_name, 
                                        last_name= last_name, 
                                        email = email, 
                                        phone_number= phone_number, 
                                        date_of_birth= date_of_birth )
                        
                        new_user.update(userid= userid)

                        #updating the booking by using Tours Class.
                        new_tour = Tours(user_id= userid, number_of_people=number_of_people )
                        new_tour.update()  

                        return jsonify(redirect_url=url_for('routes.booking', service='tour', digest=f'{newdigest}'))

                    except sqlite3.OperationalError:
                            return jsonify({"message": f"The database is currently locked. Please try again later. If the issue still persists, please inform the masjid."})  

                    except sqlite3.DatabaseError:
                        return jsonify({"message": f"An unexpected error has occured with the database. Please try again later. If the issue still persists, please inform the masjid."})                               
                    
                    except Exception as e:
                        return jsonify({"message": f"This error: {e} has occured. Please try again later to delete this booking or inform the masjid."})                         
                else:
                    try:
                        new_user = User(first_name = first_name, 
                                        last_name= last_name, 
                                        email = email, 
                                        phone_number= phone_number, 
                                        date_of_birth= date_of_birth )
                        
                        new_user.update(userid= userid) 

                        new_tour = Tours(user_id= userid, number_of_people=number_of_people )
                        new_tour.update()  

                        with sqlite3.connect('database.db') as con:
                                cur = con.cursor()
                                cur.execute(f'SELECT Digest FROM Hash WHERE UserID={userid}')
                                result = cur.fetchone()
                                digest = result[0]
                                con.commit()
                                cur.close()  

                        return jsonify(redirect_url=url_for('routes.booking', service='tour', digest=f'{digest}'))

                    except sqlite3.OperationalError:
                            return jsonify({"message": f"The database is currently locked. Please try again later. If the issue still persists, please inform the masjid."})  

                    except sqlite3.DatabaseError:
                        return jsonify({"message": f"An unexpected error has occured with the database. Please try again later. If the issue still persists, please inform the masjid."})                               
                    
                    except Exception as e:
                        return jsonify({"message": f"This error: {e} has occured. Please try again later to delete this booking or inform the masjid."})                     

    except Exception as e:
        return jsonify(redirect_url=url_for('routes.errors', errormsg = f'{e}'))
    
    return jsonify(redirect_url=url_for('routes.tours_booking'))











####################  Entire Functions Process ####################
# Route to the Function Form 
@bp.route("/functionbooking")
def function_booking():
    #Filling in the formId and actionURL for the forms
    form_id = "FunctionForm"
    action_url = url_for('routes.addfunction')
    service = "function"
    return render_template("forms/function_form.html", form_id=form_id, action_url=action_url, service = service )


#Process for Function Table which retrieves the input from the function_form.
@bp.route("/process-function", methods=['GET','POST'])
def addfunction():
    random_number = session.get('random_number') # Retrieve the stored random number in our session and if not prompt user to create one    
    if random_number:
        print(f'The verification code was generated: {random_number}')
    else:
        return jsonify({"message": f"Please press the 'Send Verifcation' button to send the code to your box first!"})
    
    try:
        if request.method == 'POST':        
            time = request.form["time"] 
            date = request.form["date"]
            if Clashed.clashed(time, date):
                return jsonify({"message": f"Unfortunately this booking is unavailable. Please re-book for another time/date.'"})
            else:
                #now verifying if the user submiited the right verification code
                verification_code = request.form["verification-code"]

                if (not verification_code.isnumeric()) or (int(verification_code) != random_number):
                    session.pop('random_number', None) # we will remove the number from session as it is now void
                    return jsonify({"message": f"Unfortunately this was not the correct code. Please try again!"})
                else:
                    session.pop('random_number', None) # we will remove the number from session as it is now void
                
                #retrieving data from the function form
                first_name = request.form["first_name"]
                last_name = request.form["last_name"]      
                email = request.form["email"]                
                phone_number = request.form["phone_number"]               
                date_of_birth = request.form["date_of_birth"]               
                post_code = request.form["post_code"]            
                address_line = request.form["address_line"]             
                payment_method = request.form.get('payment_method')            
                price = 130

                data = {'First Name': first_name, 
                        'Last Name': last_name,
                        'Email':email ,
                        'Address Line':address_line, 
                        'Post Code':post_code, 
                        'Time':time, 
                        'Date': date}
                
                invalid = Validation.validate(data= data)
                if invalid:
                    return jsonify({"message": f"{invalid}"}) 


                try:
                    #using the User Class to store the data for the User Table
                    new_user = User(first_name = first_name, 
                                    last_name= last_name, 
                                    email = email, 
                                    phone_number= phone_number, 
                                    date_of_birth= date_of_birth )
                    
                    new_user.add_User()

                    with sqlite3.connect('database.db') as con:
                            cur = con.cursor()
                            cur.execute('SELECT seq FROM sqlite_sequence WHERE name="User"')
                            result = cur.fetchone()
                            userid = result[0]
                            con.commit()
                            cur.close()

                    #calling the Function Class to store the data for the Function Table
                    new_function = Functions(user_id= userid,post_code= post_code, address_line= address_line)
                    new_function.add_Function()  
                    
                    #calling the class Payment to store the data for the Payment Table
                    new_payment = Payment(user_id= userid, post_code= post_code, address_line= address_line, payment_method= payment_method, price = price)
                    new_payment.add_Payment()

                    #calculating the digest from the hash values. We are sending this to the class Hash, and receiving the digest in return.
                    hashvalue = Hash(time = time, date = date, userid = userid)
                    digest = hashvalue.hash_algorithm()
                    digest = hashvalue.add_digest(digest)

                except sqlite3.OperationalError:
                        return jsonify({"message": f"The database is currently locked. Please try again later. If the issue still persists, please inform the masjid."})  

                except sqlite3.DatabaseError:
                    return jsonify({"message": f"An unexpected error has occured with the database. Please try again later. If the issue still persists, please inform the masjid."})                               
                
                except Exception as e:
                    return jsonify({"message": f"This error: {e} has occured. Please try again later to delete this booking or inform the masjid."})     

                try:
                    #sending the summary email after inserting all data to database
                    user_email = Email(email= email, number=(digest))
                    user_email.send_summary_email(service='function')
                    return jsonify({"message": f"Booking was successful, please check your email inbox for summary email!!'"}) #success message 

                except UnboundLocalErrors:
                    return jsonify({"message": f"A value could not be attributed. Please try again later."}) 
                
                except SocketError:
                    return jsonify({"message": f"Unfortunately the form could not send the summary email. Please try again later."}) 

                except ServerError:
                    return jsonify({"message": f"Unfortunately the server could not connect. Please check that you are connected to the Internet or try again later."})                
                except Exception:
                    return jsonify({"message": f"An unexpected error has occurred. Please contact the masjid and report this error."})  

                
    except Exception as e:
        return jsonify(redirect_url=url_for('routes.errors', errormsg = f'{e}'))
    
    return jsonify(redirect_url=url_for('routes.function_booking'))


@bp.route("/editfunctionbooking", methods=['POST','GET'])
def editfunctionbooking():
    try:
        if request.method == 'POST':
            time = request.form["time"] 
            date = request.form["date"]
            userid = request.form["UserID"]
        
            try:
                with sqlite3.connect('database.db') as con:
                        cur = con.cursor()
                        cur.execute(f'SELECT Time,Date FROM Hash WHERE UserID={userid}')
                        result = cur.fetchone()
                        con.commit()
                        cur.close()           
            except Exception as e:
                return jsonify({"message": f"This error: {e} has occured. Please try again later to delete this booking or inform the masjid."})    
            
            
            #we are now checking whether or not they have changed their booking date because if they have we need to:
            # a) Check for any existing bookings that can clash whilst excluding the current booking they have
            # b) Update the digest.
            if ((time != result[0] or date != result[1]) and (Clashed.clashed(time, date) or time =='' or date =='')):
                return jsonify({"message": f"Unfortunately this booking is unavailable. Please re-book for another time/date."})
            else:            
                #retrieving data from the editfunction form.
                first_name = request.form["first_name"]
                last_name = request.form["last_name"]
                email = request.form["email"]        
                phone_number = request.form["phone_number"]    
                date_of_birth = request.form["date_of_birth"]   
                post_code = request.form["post_code"]          
                address_line = request.form["address_line"]   

                data = {'First Name': first_name,
                        'Last Name': last_name, 
                        'Email':email,
                        'Address Line':address_line, 
                        'Post Code':post_code, 
                        'Time':time, 
                        'Date': date}


                invalid = Validation.validate(data= data)
                if invalid:
                    return jsonify({"message": f"{invalid}"}) #error message if they did not

                #updating the digest since their time/date has changed
                if (time != result[0]) or (date != result[1]):
                    hashvalue = Hash(time = time, date = date, userid = userid)
                    newdigest = hashvalue.hash_algorithm()     
                    updatehash = Hash(time = time, date=date, userid = userid)
                    updatehash.update(newdigest= newdigest)       
                                        
                    try:                                    
                        #sending them a new booking link
                        user_email = Email(email= email, number= newdigest)
                        user_email.send_summary_email(service = 'function')

                    except UnboundLocalErrors:
                        return jsonify({"message": f"A value could not be attributed. Please try again later."}) 
                    
                    except SocketError:
                        return jsonify({"message": f"Unfortunately the form could not send the summary email. Please try again later."}) 

                    except ServerError:
                        return jsonify({"message": f"Unfortunately the server could not connect. Please check that you are connected to the Internet or try again later."})                
                    except Exception:
                        return jsonify({"message": f"An unexpected error has occurred. Please contact the masjid and report this error."})                      


                    try:
                        new_user = User(first_name = first_name, 
                                        last_name= last_name, 
                                        email = email, 
                                        phone_number= phone_number, 
                                        date_of_birth= date_of_birth )
                        
                        new_user.update(userid= userid)

                        #updating the booking by sending it to the Function Class.
                        new_function = Functions(user_id= userid,post_code= post_code, address_line= address_line)
                        new_function.update()
                        return jsonify(redirect_url=url_for('routes.booking', service='function', digest=f'{newdigest}'))
                    
                    except sqlite3.OperationalError:
                            return jsonify({"message": f"The database is currently locked. Please try again later. If the issue still persists, please inform the masjid."})  

                    except sqlite3.DatabaseError:
                        return jsonify({"message": f"An unexpected error has occured with the database. Please try again later. If the issue still persists, please inform the masjid."})                               
                    
                    except Exception as e:
                        return jsonify({"message": f"This error: {e} has occured. Please try again later to delete this booking or inform the masjid."})                        
                else:

                    try:
                        new_user = User(first_name = first_name, 
                                        last_name= last_name, 
                                        email = email, 
                                        phone_number= phone_number, 
                                        date_of_birth= date_of_birth )
                        
                        new_user.update(userid= userid) 

                        new_function = Functions(user_id= userid,post_code= post_code, address_line= address_line)
                        new_function.update()   

                        with sqlite3.connect('database.db') as connection:
                                cursor = connection.cursor()
                                cursor.execute(f'SELECT Digest FROM Hash WHERE UserID={userid}')
                                result = cursor.fetchone()
                                digest = result[0]
                                connection.commit()
                                cursor.close()  
                        return jsonify(redirect_url=url_for('routes.booking', service='function', digest=f'{digest}'))
                    
                    except sqlite3.OperationalError:
                            return jsonify({"message": f"The database is currently locked. Please try again later. If the issue still persists, please inform the masjid."})  

                    except sqlite3.DatabaseError:
                        return jsonify({"message": f"An unexpected error has occured with the database. Please try again later. If the issue still persists, please inform the masjid."})                               
                    
                    except Exception as e:
                        return jsonify({"message": f"This error: {e} has occured. Please try again later to delete this booking or inform the masjid."})                        


    except Exception as e:
        return jsonify(redirect_url=url_for('routes.errors', errormsg = f'{e}'))
    
    return jsonify(redirect_url=url_for('routes.function_booking'))







####################  Entire Booking/Editing Process ####################

#Route to show the User their booking information. The dynamic URL first checks which service and then the digest.
@bp.route('/booking/<service>/<digest>')
def booking(service, digest):
    try:
        if service == 'nikah':
            try:
                # searches for the Nikah row related to the Hash digest. We join the tables User, Nikah and Hash through the foreign key UserID and use the digest to see which UserID correlates to the digest.
                with sqlite3.connect('database.db') as connection:
                    connection.row_factory = sqlite3.Row
                    cursor = connection.cursor()
                    cursor.execute(f"SELECT * FROM User JOIN Nikah ON User.UserID = Nikah.UserID JOIN Hash ON User.UserID = Hash.UserID WHERE Hash.Digest= '{digest}'")
                    rows = cursor.fetchall()        
                #if the digest never existed we return the error page
                if len(rows) == 0:
                    msg = f"It seems like you don't have a valid booking. Please feel free to make a booking."
                    return render_template("pages/error.html", errormsg = msg ) 
                return render_template("tables/nikah_table.html", rows = rows) 
            
            except sqlite3.OperationalError:
                msg = f"The database is currently locked. Please try again later. If the issue still persists, please inform the masjid."
                return render_template("pages/error.html", errormsg = msg ) 


            except sqlite3.DatabaseError:
                msg = f"An unexpected error has occured with the database. Please try again later. If the issue still persists, please inform the masjid."
                return render_template("pages/error.html", errormsg = msg )             
            
            except Exception as e:
                msg = f'This error: {e} has occured. Please try again later to delete this booking or inform the masjid.'
                return render_template('pages/error.html', errormsg = msg)        
                

        elif service == 'madrasah':
            try:
                # searches for the Madrasah row related to the Hash digest. We join the tables User, Madrasah and Hash through the foreign key UserID and use the digest to see which UserID correlates to the digest.      
                with sqlite3.connect('database.db') as connection:
                    connection.row_factory = sqlite3.Row
                    cursor = connection.cursor()
                    cursor.execute(f"SELECT * FROM User JOIN Madrasah ON User.UserID = Madrasah.UserID JOIN Hash ON User.UserID = Hash.UserID WHERE Hash.Digest='{digest}'")
                    rows = cursor.fetchall()                       
                #if the digest never existed we return the error page
                if len(rows) == 0:
                    msg = f"It seems like you don't have a valid booking. Please feel free to make a booking."
                    return render_template("pages/error.html", errormsg = msg ) 
                return render_template("tables/madrasah_table.html", rows = rows)       
            
            except sqlite3.OperationalError:
                msg = f"The database is currently locked. Please try again later. If the issue still persists, please inform the masjid."
                return render_template("pages/error.html", errormsg = msg ) 


            except sqlite3.DatabaseError:
                msg = f"An unexpected error has occured with the database. Please try again later. If the issue still persists, please inform the masjid."
                return render_template("pages/error.html", errormsg = msg )            
            
            except Exception as e:
                msg = f'This error: {e} has occured. Please try again later to delete this booking or inform the masjid.'
                return render_template('pages/error.html', errormsg = msg)                     


        elif service == 'tour':
            try:
                # searches for the Tour row related to the Hash digest. We join the tables User, Tour and Hash through the foreign key UserID and use the digest to see which UserID correlates to the digest.  
                with sqlite3.connect('database.db') as connection:
                    connection.row_factory = sqlite3.Row
                    cursor = connection.cursor()
                    cursor.execute(f"SELECT * FROM User JOIN Tours ON User.UserID = Tours.UserID JOIN Hash ON User.UserID = Hash.UserID WHERE Hash.Digest= '{digest}'")
                    rows = cursor.fetchall()                
                #if the digest never existed we return the error page
                if len(rows) == 0:
                    msg = f"It seems like you don't have a valid booking. Please feel free to make a booking."
                    return render_template("pages/error.html", errormsg = msg ) 
                return render_template("tables/tour_table.html", rows = rows)    

            except sqlite3.OperationalError:
                msg = f"The database is currently locked. Please try again later. If the issue still persists, please inform the masjid."
                return render_template("pages/error.html", errormsg = msg ) 


            except sqlite3.DatabaseError:
                msg = f"An unexpected error has occured with the database. Please try again later. If the issue still persists, please inform the masjid."
                return render_template("pages/error.html", errormsg = msg )          

            except Exception as e:
                msg = f'This error: {e} has occured. Please try again later to delete this booking or inform the masjid.'
                return render_template('pages/error.html', errormsg = msg)                 

        elif service == 'function':
            try:
                # searches for the Function row related to the Hash digest. We join the tables User, Function and Hash through the foreign key UserID and use the digest to see which UserID correlates to the digest.                  
                with sqlite3.connect('database.db') as connection:
                    connection.row_factory = sqlite3.Row
                    cursor = connection.cursor()
                    cursor.execute(f"SELECT * FROM User JOIN Function ON User.UserID = Function.UserID JOIN Hash ON User.UserID = Hash.UserID WHERE Hash.Digest= '{digest}'")
                    rows = cursor.fetchall()
                #if the digest never existed we return the error page
                if len(rows) == 0:
                    msg = f"It seems like you don't have a valid booking. Please feel free to make a booking."
                    return render_template("pages/error.html", errormsg = msg ) 
                return render_template("tables/function_table.html", rows = rows)  
            
            except sqlite3.OperationalError:
                msg = f"The database is currently locked. Please try again later. If the issue still persists, please inform the masjid."
                return render_template("pages/error.html", errormsg = msg ) 


            except sqlite3.DatabaseError:
                msg = f"An unexpected error has occured with the database. Please try again later. If the issue still persists, please inform the masjid."
                return render_template("pages/error.html", errormsg = msg )       
                
            except Exception as e:
                msg = f'This error: {e} has occured. Please try again later to delete this booking or inform the masjid.'
                return render_template('pages/error.html', errormsg = msg)               

            finally:
                cursor.close()
                connection.close()         

    except Exception as e:
        return render_template('pages/error.html', errormsg = f'Unknown error has occurred: {e}')
    
    return render_template('pages/index.html')

#Route to the edit forms. Uses the dynamic URL to determin which service form it should redirect the user to.
@bp.route("/edit/<service>", methods=['POST','GET'])
def edit(service):
    try:
        #Checks the service, pre-fills the form based on the existing dat and then redirects the user to that edit form page.
        if (request.method == 'POST' and service=='nikah'): #Checks the service and pre-fills the form based on the existing data.
            try:
                userid = request.form['userid']
                connection = sqlite3.connect("database.db")
                connection.row_factory = sqlite3.Row
                cursor = connection.cursor()
                cursor.execute(f"SELECT * FROM User JOIN Nikah ON User.UserID = Nikah.UserID JOIN Hash ON User.UserID = Hash.UserID WHERE User.UserID = {userid}")
                rows = cursor.fetchall()
                return render_template("forms/edit_forms/editnikah.html",rows=rows)     
                
            except sqlite3.OperationalError:
                msg = f"The database is currently locked. Please try again later. If the issue still persists, please inform the masjid."
                return render_template("pages/error.html", errormsg = msg ) 


            except sqlite3.DatabaseError:
                msg = f"An unexpected error has occured with the database. Please try again later. If the issue still persists, please inform the masjid."
                return render_template("pages/error.html", errormsg = msg )         

            except Exception as e:
                msg = f'This error: {e} has occured. Please try again later to delete this booking or inform the masjid.'
                return render_template('pages/error.html', errormsg = msg)                   

            finally:
                cursor.close()
                connection.close()      

            
        elif (request.method == 'POST' and service=='madrasah'):
            try:
                userid = request.form['userid']
                connection = sqlite3.connect("database.db")
                connection.row_factory = sqlite3.Row
                cursor = connection.cursor()
                cursor.execute(f"SELECT * FROM User JOIN Madrasah ON User.UserID = Madrasah.UserID JOIN Hash ON User.UserID = Hash.UserID WHERE User.UserID = {userid}")
                rows = cursor.fetchall()
                return render_template("forms/edit_forms/editmadrasah.html",rows=rows)
            
            except sqlite3.OperationalError:
                msg = f"The database is currently locked. Please try again later. If the issue still persists, please inform the masjid."
                return render_template("pages/error.html", errormsg = msg ) 


            except sqlite3.DatabaseError:
                msg = f"An unexpected error has occured with the database. Please try again later. If the issue still persists, please inform the masjid."
                return render_template("pages/error.html", errormsg = msg )        
            
            except Exception as e:
                msg = f'This error: {e} has occured. Please try again later to delete this booking or inform the masjid.'
                return render_template('pages/error.html', errormsg = msg)        

            finally:
                cursor.close()
                connection.close()      

        elif (request.method == 'POST' and service=='tour'):
            try:
                userid = request.form['userid']
                connection = sqlite3.connect("database.db")
                connection.row_factory = sqlite3.Row
                cursor = connection.cursor()
                cursor.execute(f"SELECT * FROM User JOIN Tours ON User.UserID = Tours.UserID JOIN Hash ON User.UserID = Hash.UserID WHERE User.UserID = {userid}")
                rows = cursor.fetchall()
                return render_template("forms/edit_forms/edittour.html",rows=rows)          
                
            except sqlite3.OperationalError:
                msg = f"The database is currently locked. Please try again later. If the issue still persists, please inform the masjid."
                return render_template("pages/error.html", errormsg = msg ) 


            except sqlite3.DatabaseError:
                msg = f"An unexpected error has occured with the database. Please try again later. If the issue still persists, please inform the masjid."
                return render_template("pages/error.html", errormsg = msg )  

            except Exception as e:
                msg = f'This error: {e} has occured. Please try again later to delete this booking or inform the masjid.'
                return render_template('pages/error.html', errormsg = msg)              

            finally:
                cursor.close()
                connection.close()      

            
        elif (request.method == 'POST' and service=='function'):
            #this is the edit form. We are inserting the current data into the form and will now allow the user to edit it.
            try:
                userid = request.form['userid']
                connection = sqlite3.connect("database.db")
                connection.row_factory = sqlite3.Row
                cursor = connection.cursor()
                cursor.execute(f"SELECT * FROM User JOIN Function ON User.UserID = Function.UserID JOIN Hash ON User.UserID = Hash.UserID WHERE User.UserID = {userid}")
                rows = cursor.fetchall()
                return render_template("forms/edit_forms/editfunction.html",rows=rows)     
                
            except sqlite3.OperationalError:
                msg = f"The database is currently locked. Please try again later. If the issue still persists, please inform the masjid."
                return render_template("pages/error.html", errormsg = msg ) 


            except sqlite3.DatabaseError:
                msg = f"An unexpected error has occured with the database. Please try again later. If the issue still persists, please inform the masjid."
                return render_template("pages/error.html", errormsg = msg )        
            
            except Exception as e:
                msg = f'This error: {e} has occured. Please try again later to delete this booking or inform the masjid.'
                return render_template('pages/error.html', errormsg = msg)        

            finally:
                cursor.close()
                connection.close()      

    except Exception as e:
        return render_template('pages/error.html', errormsg = f'Unknown error has occurred: {e}')
    
    return render_template('pages/index.html')
           
###### DELETING THE BOOKING #####
#Route to delete the booking from a Table.
@bp.route("/delete/<service>", methods=['POST','GET'])
def delete(service):
    try:
        #The dynamic URL tells us which service Table the record needs to be deleted from.
        if (request.method == 'POST' and service =='nikah'):
            try:
                userid = request.form['userid']
                deletebooking = Nikah.delete(userid=userid) # Nikah Class deletes the record.
                return(f'{deletebooking}')
            except Exception as e:
                msg = f'This error: {e} has occured. Please try again later to delete this booking or inform the masjid.'
                return render_template('pages/error.html', errormsg = msg)
        
        elif (request.method == 'POST' and service =='madrasah'):
            try:
                userid = request.form['userid']
                deletebooking = Madrasah.delete(userid=userid) # Madrasah Class deletes the record.
                return(f'{deletebooking}')
            except Exception as e:
                msg = f'This error: {e} has occured. Please try again later to delete this booking or inform the masjid.'
                return render_template('pages/error.html', errormsg = msg)

        elif (request.method == 'POST' and service == 'tour'):
            try:
                userid = request.form['userid']   
                deletebooking = Tours.delete(userid = userid) # Tour Class deletes the record.
                return(f'{deletebooking}')
            except Exception as e:
                msg = f'This error: {e} has occured. Please try again later to delete this booking or inform the masjid.'
                return render_template('pages/error.html', errormsg = msg)

        elif (request.method == 'POST' and service == 'function'):
            try:
                userid = request.form['userid']   
                deletebooking = Functions.delete(userid = userid) # Function Class deletes the record.
                return(f'{deletebooking}')
            except Exception as e:
                msg = f'This error: {e} has occured. Please try again later to delete this booking or inform the masjid.'
                return render_template('pages/error.html', errormsg = msg)
    except Exception as e:
        return render_template('pages/error.html', errormsg = f'Unknown error has occurred: {e}')
    
    return render_template('pages/index.html')
