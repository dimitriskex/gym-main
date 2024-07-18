from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
import mysql.connector
from datetime import datetime, timedelta
import os



app = Flask(__name__)
app.secret_key = os.urandom(24)

db_config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '',
        'database': 'gymdb',
    }

    # Establish a connection to MySQL
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()
 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        cursor.execute("SELECT MAX(userid) FROM users")
        max_userid = cursor.fetchone()[0]
        if max_userid is None:
            userid = 1
        else:
            userid = max_userid + 1
        
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        country = request.form['country']
        city = request.form['city']
        address = request.form['address']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        status = "Pending"
        role = "User"

        # Insert user into the users table
        cursor.execute("INSERT INTO users (userid, firstname, lastname, country, city, address, email, username, password, status, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (userid, firstname, lastname, country, city, address, email, username, password, status, role))
        connection.commit()
        
        return redirect(url_for('login'))
    return render_template('new_register.html')


def is_user_authenticated():
    return 'username' in session

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Retrieve user from the users table
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        
        if user:
            session['username'] = username
            return redirect(url_for('main'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/logout')
def logout():
    if is_user_authenticated():
        username = session.get('username')  # Assuming the username is stored in the session
        session.pop('username', None)
        flash(f'Logged out successfully, {username}!', 'success')
    else:
        flash('You are not logged in.', 'info')
    return redirect(url_for('login'))
    
def execute_query(query):

    cursor.execute(query)
    data = cursor.fetchall()
    # cursor.close()
    # connection.close()

    return data




def admin_check():
    username = session.get('username')
    if username == None:
        return False
    else:
        cursor.execute("SELECT userid FROM users WHERE username = %s", (username, ))
        admin_userid = cursor.fetchone()[0]

        cursor.execute("SELECT role FROM users WHERE userid = %s", (admin_userid, ))
        is_admin = cursor.fetchone()[0]
        return is_admin == 'Trainer'

@app.route('/')
def main():
    return render_template('new_index.html')



'''
B1
Περιήγηση στις υπηρεσίες του γυμναστηρίου. Ένας απλός χρήστης του συστήματος θα μπορεί να 
προβάλει λίστα με τις υπηρεσίες που προσφέρει το γυμναστήριο (όχι το πρόγραμμα των 
προγραμμάτων όμως) χωρίς να είναι εγγεγραμμένος στο σύστημα και χωρίς να έχει εισέλθει σε αυτό 
με το username και το password του.
'''
@app.route('/gym_services')
def view_gym_services():
    query = "SELECT * FROM gymservices"
    gym_services=execute_query(query)
    
    return render_template('new_gym_services.html', gym_services=gym_services)

'''
B2
Κράτηση προϊόντος/ υπηρεσίας. Η χρήση των υπηρεσιών του γυμναστηρίου θα γίνεται μόνο με 
ραντεβού. Εάν ένας χρήστης επιθυμεί να κλείσει ραντεβού σε κάποιο από τα ατομικά ή τα ομαδικά 
προγράμματα του γυμναστηρίου θα πρέπει πρώτα να εισέρχεται στο σύστημα με τα στοιχεία του. 
Αρχικά θα κάνει αναζήτηση διαθεσιμότητας με βάση το πρόγραμμα που επιθυμεί και την ημερομηνία. 
Εάν υπάρχει κενή θέση στο time slot που επιθυμεί θα μπορεί να κλείσει ραντεβού διαφορετικά θα 
πρέπει να επιλέξει άλλο time slot.Ο χρήστης θα μπορεί να ακυρώσει το ραντεβού του μέχρι και 2 ώρες 
πριν από την ώρα έναρξης, ενώ εάν κάνει 2 ακυρώσεις μέσα στην εβδομάδα δε θα του δίνεται το 
δικαίωμα να κλείσει ραντεβού για κάποια από τις υπόλοιπες μέρες τις εβδομάδας.
'''
@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    try:
        if not is_user_authenticated():
            return redirect(url_for('login'))
    
        if request.method == 'POST':
            programid = request.form.get('programid')

            if programid:
                cursor.execute("SELECT programid FROM programs WHERE programid = %s", (programid,))
                existing_program = cursor.fetchone()
                
                if existing_program:
                    programtime = request.form.get('programtime')
                    cursor.execute("SELECT programtime FROM programs WHERE programtime = %s", (programtime,)) 
                    existing_date_time = cursor.fetchone()

                    if existing_date_time:
                        cursor.execute("SELECT capacity FROM programs WHERE programtime = %s", (programtime,)) 
                        existing_capacity = cursor.fetchone()[0]
                        
                        if existing_capacity > 0 :
                            cursor.execute("UPDATE programs SET capacity = %s WHERE programid = %s", (existing_capacity - 1, programid))
                            connection.commit()

                            cursor.execute("SELECT userid FROM users WHERE username = %s", (session['username'], ))
                            reservation_userid = cursor.fetchone()[0]
                            print("session['username'] = ", session['username'])
                            print("reservation_userid = ", reservation_userid)

                            # Inserting reservation without specifying reservationid
                            cursor.execute("INSERT INTO reservations (userid, programid, status) VALUES (%s, %s, %s)", (reservation_userid, programid, "Pending"))
                            connection.commit()
                            print("INSERT INTO reservations (userid, programid, status) VALUES (%s, %s, %s)", (reservation_userid, programid, "Pending"))

                            # Retrieving the reservationid of the most recently inserted record
                            cursor.execute("SELECT LAST_INSERT_ID()")
                            new_reservation_id = cursor.fetchone()[0]

                            print("New Reservation ID:", new_reservation_id)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    return render_template('reservation_search.html')


user_cancelations = {}

@app.route('/reservations_cancel', methods=['GET', 'POST'])
def reservations_cancel():
    try:
        if not is_user_authenticated():
            return redirect(url_for('login'))
        if request.method == 'POST':
            programid = request.form.get('programid')

            if programid:
                
                cursor.execute("SELECT programid FROM programs WHERE programid = %s", (programid,))
                existing_program = cursor.fetchone()
                
                if existing_program:
                    programtime = request.form.get('programtime')
                    
                    cursor.execute("SELECT programtime FROM programs WHERE programtime = %s", (programtime,))
                    existing_date_time = cursor.fetchone()
                    print("existing_date_time = ", existing_date_time)

                    if existing_date_time:
                        # Έλεγχος για την ακύρωση ραντεβού
                        appointment_time = datetime.strptime(programtime, '%Y-%m-%dT%H:%M')
                        print("appointment_time = ", appointment_time)
                        current_time = datetime.now()
                        print("current_time = ", current_time)
                        cancellation_deadline = appointment_time - timedelta(hours=2)
                        print("cancellation_deadline = ", cancellation_deadline)

                        if current_time < cancellation_deadline:
                            if session['username'] not in user_cancelations:
                                user_cancelations[session['username']] = 0

                            print("ok6")
                            user_cancelations[session['username']] += 1
                            print("user_cancelations[session['username']] = ", user_cancelations[session['username']])

                            cursor.execute("SELECT userid FROM users WHERE username = %s", (session['username'], ))
                            reservation_userid = cursor.fetchone()[0]

                            
                            # Έλεγχος για τον περιορισμό ακυρώσεων σε μία εβδομάδα
                            if user_cancelations[session['username']] <= 2:
                                cursor.execute("DELETE FROM reservations WHERE userid = %s AND programid = %s", (reservation_userid, programid, ))
                                print("DELETE FROM reservations WHERE userid = %s AND programid = %s", (reservation_userid, programid, ))
                                connection.commit()
                            else:
                                return jsonify({'error': 'Έχετε υπερβεί το μέγιστο αριθμό ακυρώσεων για αυτήν την εβδομάδα'}), 400
                        else:
                            return jsonify({'error': 'Not able to delete'}), 400

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    return render_template('reservation_search.html')


@app.route('/reservation_search')
def reservation_search():
    return render_template('reservation_search.html')



'''
B3
Νέα/ανακοινώσεις. Ο χρήστης θα μπορεί να βλέπει νέα και ανακοινώσεις που έχουν αναρτηθεί από το γυμναστήριο.
'''
@app.route('/announcements')
def view_announcements():
    query = "SELECT * FROM announcements"
    announcements=execute_query(query)
    
    return render_template('new_announcements.html', announcements=announcements)

'''
B4
Ιστορικό κρατήσεων: Ο χρήστης θα μπορεί να δει λίστα με όλες τις κρατήσεις που έχει κάνει στο σύστημα μέχρι τη στιγμή εκείνη.
'''
@app.route('/reservation_history')
def reservation_history():
    if not is_user_authenticated():
        return redirect(url_for('login'))
    
    query = "SELECT * FROM reservations"
    reservations=execute_query(query)

    return render_template('reservation_history.html', reservations=reservations)




@app.route('/admin_general')
def admin_general():
    if not admin_check():
        return redirect(url_for('login'))
    return render_template('admin_general.html')

@app.route('/A1_button')
def A1_button():
    return render_template('A1_button.html')

@app.route('/A2_button')
def A2_button():
    return render_template('A2_button.html')

@app.route('/A3_button')
def A3_button():
    return render_template('A3_button.html')

@app.route('/A4_button')
def A4_button():
    return render_template('A4_button.html')

@app.route('/create_button_a2')
def create_button_a2():
    return render_template('create_button_a2.html')

@app.route('/create_button_a3_programs')
def create_button_a3_programs():
    return render_template('create_button_a3_programs.html')

@app.route('/create_button_a3_trainers')
def create_button_a3_trainers():
    return render_template('create_button_a3_trainers.html')

@app.route('/create_button_a4')
def create_button_a4():
    return render_template('create_button_a4.html')

@app.route('/manage_button_a1')
def manage_button_a1():
    return render_template('manage_button_a1.html')

@app.route('/delete_button_a2')
def delete_button_a2():
    return render_template('delete_button_a2.html')

@app.route('/delete_button_a3_programs')
def delete_button_a3_programs():
    return render_template('delete_button_a3_programs.html')

@app.route('/delete_button_a3_trainers')
def delete_button_a3_trainers():
    return render_template('delete_button_a3_trainers.html')

@app.route('/delete_button_a4')
def delete_button_a4():
    return render_template('delete_button_a4.html')

@app.route('/update_button_a2')
def update_button_a2():
    return render_template('update_button_a2.html')

@app.route('/update_button_a3_programs')
def update_button_a3_programs():
    return render_template('update_button_a3_programs.html')

@app.route('/update_button_a3_trainers')
def update_button_a3_trainers():
    return render_template('update_button_a3_trainers.html')

@app.route('/update_button_a4')
def update_button_a4():
    return render_template('update_button_a4.html')




'''
A1
Διαχείριση αιτημάτων εγγραφής στο σύστημα: Ο διαχειριστής του συστήματος θα έχει πρόσβαση 
στα αιτήματα για εγγραφή στο σύστημα και να τα εγκρίνει ή να τα απορρίπτει. Η διαδικασία εγγραφής 
των χρηστών περιγράφεται αναλυτικά παρακάτω.
'''
@app.route('/status_view', methods=['GET'])
def status_view():
    users = execute_query("SELECT * FROM users")
    return render_template('A1_button.html', users=users)

@app.route('/status_manage', methods=['GET', 'POST'])
def status_manage():
    try:
        if request.method == 'POST':
            userid = request.form.get('userid')

            if userid:
                cursor.execute("SELECT userid FROM users WHERE userid = %s", (userid,))
                existing_user = cursor.fetchone()

                if existing_user:
                    status = request.form.get('status')
                    cursor.execute("UPDATE users SET status= %s WHERE userid = %s", (status, userid, ))
                    connection.commit()

        return redirect(url_for('status_view'))
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    return "Error updating user", 500  # Return an HTTP 500 error response

'''
Α2
Διαχείριση χρηστών συστήματος: Ο διαχειριστής του συστήματος θα έχει πρόσβαση στους χρήστες 
του συστήματος και θα έχει την ευθύνη της ενημέρωσης των στοιχείων τους στη βάση δεδομένων 
(Create Read Update Delete - CRUD operations). Επίσης θα έχει τη δυνατότητα να αναθέσει ή να 
τροποποιεί το ρόλο ενός χρήστη
'''
@app.route('/users_view', methods=['GET'])
def users_view():
    users = execute_query("SELECT * FROM users")
    return render_template('A2_button.html', users=users)

@app.route('/users_create', methods=['GET', 'POST'])
def users_create():
    if request.method == 'POST':
        userid = request.form['userid']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        country = request.form['country']
        city = request.form['city']
        address = request.form['address']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
         

        # Insert user into the users table
        cursor.execute("INSERT INTO users (userid, firstname, lastname, country, city, address, email, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (userid, firstname, lastname, country, city, address, email, username, password))
        connection.commit()

    return redirect(url_for('users_view'))
    
@app.route('/users_update', methods=['POST'])
def users_update():
    try:
        if request.method == 'POST':
            userid = request.form.get('userid')

            if userid:
                cursor.execute("SELECT userid FROM users WHERE userid = %s", (userid,))
                existing_user = cursor.fetchone()

                if existing_user:
                    firstname = request.form.get('firstname')
                    lastname = request.form.get('lastname')
                    country = request.form.get('country')
                    city = request.form.get('city')
                    address = request.form.get('address')
                    email = request.form.get('email')
                    username = request.form.get('username')
                    password = request.form.get('password')
                    role = request.form.get('role')

                    # Using a parameterized query to prevent SQL injection
                    cursor.execute("UPDATE users SET firstname = %s, lastname = %s, country = %s, city = %s, address = %s, email = %s, username = %s, password = %s, role = %s WHERE userid = %s",
                                   (firstname, lastname, country, city, address, email, username, password, role, userid))
                    connection.commit()

                    if role == "Trainer":
                        cursor.execute("INSERT INTO trainers (trainerid, trainername) VALUES (%s, %s)", (userid, firstname + lastname, ))

                    return redirect(url_for('users_view'))

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    return "Error updating user", 500  # Return an HTTP 500 error response

@app.route('/users_delete', methods=['GET', 'POST'])
def users_delete():
    if request.method == 'POST':
        userid = request.form['userid']
        query = "SELECT userid FROM users WHERE userid = %s"
        try:
            cursor.execute(query, (userid,))
            existing_user = cursor.fetchone()

            if existing_user:
                # Correct DELETE syntax (remove the '*')
                cursor.execute("DELETE FROM users WHERE userid = %s", (userid,))
                connection.commit()
        except Exception as e:
            # Handle exceptions (print, log, or return an error response)
            print(f"Error: {e}")

        return redirect(url_for('users_view'))

'''
A3
Διαχείριση δομικών στοιχείων του συστήματος: Ο διαχειριστής του συστήματος θα έχει πρόσβαση 
σε όλα τα στοιχεία του συστήματος του γυμναστηρίου που σχετίζονται με τις υπηρεσίες που αυτό 
προσφέρει στους χρήστες και, πιο συγκεκριμένα, θα έχει την ευθύνη της ενημέρωσης των στοιχείων 
αυτών στη βάση δεδομένων (Create Read Update Delete - CRUD operations). 
Μεταξύ των στοιχείων που θα διαχειρίζεται είναι:
• οι γυμναστές 
• τα προγράμματα που προσφέρονται (π.χ. pilates, ενδυνάμωση, πισίνα). 
• Το πρόγραμμα για τα ομαδικά προγράμματα (ημέρα, ώρα, γυμναστής). 
Για κάθε πρόγραμμα θα πρέπει να καταχωρείται μέγιστη χωρητικότητα ατόμων.
'''
@app.route('/trainers_view', methods=['GET'])
def trainers_view():
    trainers = execute_query("SELECT * FROM trainers")
    return render_template('trainers_view.html', trainers=trainers)

@app.route('/trainers_create', methods=['GET', 'POST'])
def trainers_create():
    if request.method == 'POST':
        trainerid = request.form['trainerid']
        trainername = request.form['trainername']
        cursor.execute("INSERT INTO trainers (trainerid, trainername) VALUES (%s, %s)", (trainerid, trainername))
        connection.commit()

        return redirect(url_for('trainers_view'))
    
@app.route('/trainers_update', methods=['POST'])
def trainers_update():
    try:
        if request.method == 'POST':
            trainerid = request.form.get('trainerid')

            if trainerid:
                cursor.execute("SELECT trainerid FROM trainers WHERE trainerid = %s", (trainerid,))
                existing_trainer = cursor.fetchone()

                if existing_trainer:
                    trainername = request.form.get('trainername')

                    cursor.execute("UPDATE trainers SET trainername = %s WHERE trainerid = %s", (trainername, trainerid))
                    connection.commit()

                    return redirect(url_for('trainers_view'))

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    return "Error updating trainer", 500  

@app.route('/trainers_delete', methods=['GET', 'POST'])
def trainers_delete():
    if request.method == 'POST':
        trainerid = request.form['trainerid']
        query = "SELECT trainerid FROM trainers WHERE trainerid = %s"
        
        try:
            cursor.execute(query, (trainerid,))
            existing_user = cursor.fetchone()

            if existing_user:
                cursor.execute("DELETE FROM gymservices WHERE trainers_trainerid = %s", (trainerid,))
                cursor.execute("DELETE FROM trainers WHERE trainerid = %s", (trainerid,))
                connection.commit()
        except Exception as e:
            print(f"Error: {e}")

        return redirect(url_for('trainers_view'))

@app.route('/programs_view', methods=['GET'])
def programs_view():
    programs = execute_query("SELECT * FROM programs")
    return render_template('programs_view.html', programs=programs)

@app.route('/program_create', methods=['GET', 'POST'])
def program_create():
    if request.method == 'POST':
        programid = request.form['programid']
        programname = request.form['programname']
        capacity = request.form['capacity']
        cursor.execute("INSERT INTO programs (programid, programname, capacity) VALUES (%s, %s, %s)", (programid, programname, capacity))
        connection.commit()
        
    return redirect(url_for('programs_view'))
    
@app.route('/program_update', methods=['POST'])
def program_update():
    try:
        if request.method == 'POST':
            programid = request.form.get('programid')

            if programid:
                cursor.execute("SELECT programid FROM programs WHERE programid = %s", (programid,))
                existing_program = cursor.fetchone()

                if existing_program:
                    programname = request.form.get('programname')
                    capacity = request.form.get('capacity')

                    # Using a parameterized query to prevent SQL injection
                    cursor.execute("UPDATE programs SET programname = %s, capacity = %s WHERE programid = %s",
                                   (programname, capacity, programid))
                    connection.commit()

                    return redirect(url_for('programs_view'))

    except mysql.connector.Error as err:
        print(f"Error updating program: {err}")

    return "Error updating program", 500  # Return an HTTP 500 error response

@app.route('/program_delete', methods=['GET', 'POST'])
def program_delete():
    if request.method == 'POST':
        programid = request.form['programid']
        query = "SELECT programid FROM programs WHERE programid = %s"
        try:
            cursor.execute(query, (programid,))
            existing_user = cursor.fetchone()

            if existing_user:
                cursor.execute("DELETE FROM programs WHERE programid = %s", (programid,))
                connection.commit()
        except Exception as e:
            print(f"Error: {e}")

        return redirect(url_for('programs_view'))

'''
A4
Διαχείριση ανακοινώσεων/ προσφορών. Ο διαχειριστής θα μπορεί να αναρτά ανακοινώσεις και 
προσφορές οι οποίες θα είναι ορατές μόνο από τους εγγεγραμμένους χρήστες. Επίσης θα μπορεί να 
τροποποιεί και να διαγράφει ανακοινώσεις.
'''
@app.route('/announcements_view', methods=['GET'])
def announcements_view():
    announcements = execute_query("SELECT * FROM announcements")
    return render_template('A4_button.html', announcements=announcements)

@app.route('/announcement_create', methods=['GET', 'POST'])
def announcement_create():
    if request.method == 'POST':
        announcementid = request.form['announcementid']
        announcementtext = request.form['announcementtext']
        createdat = request.form['createdat']
        userid = request.form['userid']

        cursor.execute("INSERT INTO announcements (announcementid, announcementtext, createdat, userid) VALUES (%s, %s, %s, %s)", (announcementid, announcementtext, createdat, userid))
        connection.commit()
    return redirect(url_for('announcements_view'))

@app.route('/announcement_delete', methods=['GET', 'POST'])
def announcement_delete():
    if request.method == 'POST':
        announcementid = request.form['announcementid']
        query = "SELECT announcementid FROM announcements WHERE announcementid = %s"
        try:
            cursor.execute(query, (announcementid,))
            existing_user = cursor.fetchone()

            if existing_user:
                cursor.execute("DELETE FROM announcements WHERE announcementid = %s", (announcementid,))
                connection.commit()
        except Exception as e:
            print(f"Error: {e}")

        return redirect(url_for('announcements_view'))

@app.route('/announcement_update', methods=['POST'])
def announcement_update():
    try:
        if request.method == 'POST':
            announcementid = request.form.get('announcementid')

            if announcementid:
                cursor.execute("SELECT announcementid FROM announcements WHERE announcementid = %s", (announcementid,))
                existing_announcement = cursor.fetchone()

                if existing_announcement:
                    announcementtext = request.form.get('announcementtext')
                    createdat = request.form.get('createdat')
                    userid = request.form.get('userid')

                    # Using a parameterized query to prevent SQL injection
                    cursor.execute("UPDATE announcements SET announcementtext = %s, createdat = %s, userid = %s WHERE announcementid = %s",
                                   (announcementtext, createdat, userid, announcementid))
                    connection.commit()
                    return redirect(url_for('announcements_view'))

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    return redirect(url_for('announcements_view'))









if __name__ == '__main__':
    app.run(debug=True)
