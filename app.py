from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
import psycopg2
import bcrypt
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

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

        cur = conn.cursor()
        cur.execute("SELECT name, password FROM member WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user:
            name, hashed_password = user
            if sha256_crypt.verify(password, hashed_password):
                session['name'] = name
                flash("Successfully signed in!")
                return redirect(url_for('account'))
        
        flash("Cannot sign in - incorrect email or password.")
    
    return render_template('signin.html')

@app.route('/account')
def account():
    if 'name' in session:
        name = session['name']
        return render_template('account.html', name=name)
    else:
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

@app.route('/checkout_books', methods=['GET', 'POST'])
def checkout_books():
    if request.method == 'POST':
        # Logic to handle checking out books
        flash("Books checked out successfully!")
        return redirect(url_for('account'))
    else:
        # Render the checkout books page
        return render_template('checkout_books.html')



@app.route('/employee/signin')
def employee_signin():
    # Add functionality for employee signin page
    return "Employee Sign In Page"

@app.route('/view_books')
def view_books():
    # Add functionality for viewing library books
    return "View Library Books Page"

if __name__ == '__main__':
    app.run(debug=True)
