from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
import psycopg2
import bcrypt
from passlib.hash import sha256_crypt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.permanent_session_lifetime = datetime.timedelta(hours=2)  # Set session timeout to 2 hours

# PostgreSQL connection configuration
conn = psycopg2.connect(
    host="localhost",
    database="library",
    user="postgres",
    password="password"
)

'''
# connection to db
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:password@localhost/students'
db=SQLAlchemy(app)
'''

class SignUpForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=100)])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=255)])
    student = BooleanField('Student')
    teacher = BooleanField('Teacher')
    contact_number = StringField('Contact Number', validators=[InputRequired(), Length(max=20)])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = sha256_crypt.encrypt(request.form['password'])  # Encrypt password
        contact = request.form['contact']
        member_type = request.form['member_type']

        cur = conn.cursor()
        cur.execute("INSERT INTO member (name, email, password, member_type, contact) VALUES (%s, %s, %s, %s, %s)",
                    (name, email, password, member_type, contact))
        conn.commit()
        cur.close()
        
        return redirect(url_for('index'))

    return render_template('signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        session.permanent = True  # Mark session as permanent
        session['user'] = {'email': email}  # Store user's email in session
        
        

        cur = conn.cursor()
        cur.execute("SELECT name, password, id FROM member WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user:
            name, hashed_password, idnum = user
            if sha256_crypt.verify(password, hashed_password):
                session['name'] = name
                session['user_id'] = idnum
                flash("Successfully signed in!")
                return redirect(url_for('account'))
        
        flash("Cannot sign in - incorrect email or password.")
        #return redirect(url_for('account'))
    
    return render_template('signin.html')
'''
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        # Authentication logic here
        
        # If authentication is successful, set user session
        session.permanent = True  # Mark session as permanent
        session['user'] = {'email': email}  # Store user's email in session
        flash("You are now signed in.")
        return redirect(url_for('account'))
    
    return render_template('signin.html')
'''
'''
@app.route('/account')
def account():
    if 'name' in session:
        name = session['name']
        return render_template('account.html', name=name)
    else:
        return redirect(url_for('signin'))
    
'''
@app.route('/account')
def account():
    if 'user' in session:
        return render_template('account.html')
    else:
        return redirect(url_for('signin'))
    
@app.route('/signout')
def signout():
    session.pop('user', None)  # Clear user session
    flash("You have been signed out.")
    return redirect(url_for('signin'))


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    #if 'user' not in session:
    #    return redirect(url_for('signin'))  # Redirect to sign-in if not logged in
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        contact = request.form['contact']

        cur = conn.cursor()
        # Update user information in the database
        if password:
            hashed_password = sha256_crypt.encrypt(password)
            cur.execute("UPDATE member SET name=%s, email=%s, password=%s, contact=%s WHERE email=%s",
                        (name, email, hashed_password, contact, session['user']['email']))
        else:
            cur.execute("UPDATE member SET name=%s, email=%s, contact=%s WHERE email=%s",
                        (name, email, contact, session['user']['email']))
        
        conn.commit()
        cur.close()

        # Update session user information
        session['user']['name'] = name
        session['user']['email'] = email
        session['user']['contact'] = contact

        flash("Profile updated successfully!")
        return redirect(url_for('account'))
    else:
        return render_template('edit_profile.html', user=session['user'])

'''
@app.route('/checkout_books', methods=['GET', 'POST'])
def checkout_books():
    if request.method == 'GET':
        cur = conn.cursor()
        cur.execute("SELECT * FROM books")
        books = cur.fetchall()
        cur.close()

        return render_template('checkout_books.html', books=books)
    elif request.method == 'POST':
        # Handle book checkout logic here
        pass

'''
@app.route('/checkout_books', methods=['GET', 'POST'])
def checkout_books():
    if request.method == 'GET':
        cur = conn.cursor()
        cur.execute("SELECT * FROM books")
        books = cur.fetchall()
        cur.close()

        return render_template('checkout_books.html', books=books)
    elif request.method == 'POST':
        book_id = request.form.get('book_id')
        if book_id:
            # Update book status to "Not Available" in the database
            cur = conn.cursor()
            cur.execute("UPDATE books SET status='not available' WHERE id=%s", (book_id,))
            conn.commit()
            cur.close()
            flash("Book checked out successfully!")
        else:
            flash("Invalid book ID!")

        return redirect(url_for('checkout_books'))
    
@app.route('/view_checked_out_books', methods=['GET', 'POST'])
def view_checked_out_books():
    if request.method == 'GET':
        # Fetch checked out books for the current user (assuming you have a user ID in the session)
        user_id = session.get('user_id')  # Adjust this according to your session setup
        print(user_id)
        if user_id:
            cur = conn.cursor()
            cur.execute("SELECT * FROM books WHERE status='not available' AND id=%s", (user_id,))
            checked_out_books = cur.fetchall()
            cur.close()
            return render_template('view_checked_out_books.html', checked_out_books=checked_out_books)
        #else:
        #    flash("You need to sign in to view checked out books.")
        #    return redirect(url_for('signin'))
    elif request.method == 'POST':
        book_id = request.form.get('book_id')
        if book_id:
            # Update book status to "Available" in the database
            cur = conn.cursor()
            cur.execute("UPDATE books SET status='available' WHERE id=%s", (book_id,))
            conn.commit()
            cur.close()
            flash("Book returned successfully!")
            return redirect(url_for('view_checked_out_books'))
        else:
            flash("Invalid book ID!")
            return redirect(url_for('view_checked_out_books'))


@app.route('/employee/signin')
def employee_signin():
    # Add functionality for employee signin page
    return "Employee Sign In Page"

@app.route('/view_books')
def view_library_books():
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    cur.close()
    
    return render_template('view_books.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)
