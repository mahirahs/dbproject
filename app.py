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
                session['id'] = idnum
                flash("Successfully signed in!")
                return redirect(url_for('account'))
        
        flash("Cannot sign in - incorrect email or password.")
        #return redirect(url_for('account'))
    
    return render_template('signin.html')

@app.route('/account')
def account():
    if 'user' in session:
        #return render_template('account.html')
        user_id = session['id']  # Assuming the user ID is stored in the session
        cur = conn.cursor()
        #cur.execute("SELECT COALESCE(SUM(CAST(fineincurred AS NUMERIC)), 0) FROM book_record WHERE memberid = %s", (user_id,))
        #total_fine = cur.fetchone()[0]  # Fetching the total fine incurred
        #cur.close()
        cur.execute("""
            SELECT m.id, m.name, COALESCE(SUM(CAST(br.fineincurred AS NUMERIC)), 0) AS total_fine
            FROM member AS m
            LEFT JOIN book_record AS br ON m.id = br.memberid
            WHERE m.id = %s
            GROUP BY m.id, m.name;
        """, (user_id,))
        total_fine = cur.fetchone()  # Fetching the total fine incurred by the member
        cur.close()
        return render_template('account.html', total_fine=total_fine)
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


@app.route('/checkout_books', methods=['GET', 'POST'])
def checkout_books():
    if request.method == 'GET':
        cur = conn.cursor()
        cur.execute("SELECT * FROM books WHERE status='available'")
        available_books = cur.fetchall()
        cur.close()
        return render_template('checkout_books.html', books=available_books)
    elif request.method == 'POST':
        book_id = request.form.get('book_id')
        if book_id:
            # Update book status to "Not Available" in the database
            cur = conn.cursor()

            cur.execute("UPDATE books SET status='not available' WHERE id=%s", (book_id,))
            
            # Insert record into book_record table
            borrow_date = datetime.date.today()
            return_date = borrow_date + datetime.timedelta(days=10)  # Assuming 10 days borrowing period
            cur.execute("INSERT INTO book_record (bookid, memberid, borrowdate, returndate, isreturned) VALUES (%s, %s, %s, %s, true)",
                        (book_id, session['id'], borrow_date, return_date))
            # Update isreturned attribute to false in the book_record table
            cur.execute("UPDATE book_record SET isreturned=false WHERE bookid=%s AND memberid=%s", (book_id, session['id']))
            conn.commit()
            cur.close()
            flash("Book checked out successfully!")
        else:
            flash("Invalid book ID!")

        return redirect(url_for('checkout_books'))

@app.route('/view_checked_out_books', methods=['GET'])
def view_checked_out_books():
    '''if 'user' in session:
        user_id = session['id']  # Assuming the user ID is stored in the session
        cur = conn.cursor()
        cur.execute("SELECT books.id, books.name, books.author, books.publisher, book_record.borrowdate, book_record.returndate, book_record.dayspast, book_record.fineincurred FROM books INNER JOIN book_record ON books.id = book_record.bookid WHERE book_record.memberid = %s AND book_record.isreturned = false", (user_id,))
        checked_out_books = cur.fetchall()
        cur.close()
        return render_template('view_checked_out_books.html', checked_out_books=checked_out_books)
    '''
    if 'user' in session:
        user_id = session['id']  # Assuming the user ID is stored in the session
        cur = conn.cursor()
        # Query to count the total number of books borrowed by the signed-in member
        cur.execute("SELECT COUNT(*) FROM book_record WHERE memberid = %s AND isreturned = false", (user_id,))
        total_books_borrowed = cur.fetchone()[0]  # Fetching the total number of books borrowed
        # Query to retrieve the list of checked-out books
        cur.execute("""
            SELECT books.id, books.name, books.author, books.publisher, book_record.borrowdate, book_record.returndate, book_record.dayspast, book_record.fineincurred
            FROM books
            INNER JOIN book_record ON books.id = book_record.bookid
            WHERE book_record.memberid = %s AND book_record.isreturned = false
        """, (user_id,))
        checked_out_books = cur.fetchall()
        cur.close()
        return render_template('view_checked_out_books.html', checked_out_books=checked_out_books, total_books_borrowed=total_books_borrowed)
    else:
        flash("You need to sign in to view checked out books.")
        return redirect(url_for('signin'))
        
@app.route('/return_book', methods=['POST'])
def return_book():
    record_id = request.form.get('record_id')
    
    # get user id and book id
    user_id = session['id']
    book_id = request.form.get('book_id')
    
    if user_id and book_id:
        cur = conn.cursor()
        # Fetch book ID and user ID from book_record table
        #cur.execute("SELECT bookid, memberid FROM book_record WHERE id = %s", (record_id,))
        #record = cur.fetchone()
        #book_id = record[0]
        #member_id = record[1]

        # Update book status to "Available" in the books table
        cur.execute("UPDATE books SET status='available' WHERE id=%s", (book_id,))

        # Update isreturned attribute to true in the book_record table
        cur.execute("UPDATE book_record SET isreturned=true WHERE bookid=%s", (book_id,))
        
        conn.commit()
        cur.close()
        flash("Book returned successfully!")
    else:
        flash("Invalid record ID!")
    return redirect(url_for('view_checked_out_books'))

@app.route('/employee_signup', methods=['GET', 'POST'])
def employee_signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = sha256_crypt.encrypt(request.form['password'])  # Encrypt password
        contact = request.form['contact']
        #member_type = request.form['member_type']

        cur = conn.cursor()
        cur.execute("INSERT INTO employee (name, email, password, contact) VALUES (%s, %s, %s, %s)",
                    (name, email, password, contact))
        conn.commit()
        cur.close()
        
        return redirect(url_for('index'))

    return render_template('employee_signup.html')

@app.route('/employee_signin', methods=['GET', 'POST'])
def employee_signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        session.permanent = True  # Mark session as permanent
        session['user'] = {'email': email}  # Store user's email in session

        cur = conn.cursor()
        cur.execute("SELECT name, password, id FROM employee WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user:
            
            #idnum, name, email, password_this, contact = user
            name, hashed_password, idnum = user
            #name, hashed_password, idnum = user
            if sha256_crypt.verify(password, hashed_password):
                print("HERE pass")
                session['name'] = name
                session['id'] = idnum
                flash("Successfully signed in!")
                return redirect(url_for('dashboard'))
        
        flash("Cannot sign in - incorrect email or password.")
        #return redirect(url_for('dashboard'))
    else:
        print("at else")
        return render_template('employee_signin.html')

# Route for employee dashboard
@app.route('/dashboard')
def dashboard():
    
    if 'user' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('signin'))
     

# Route for employee sign-out
@app.route('/employee_signout')
def employee_signout():
    session.pop('user', None)
    return redirect(url_for('employee_signin'))

# Route to view member details and their checked-out books
@app.route('/view_members')
def view_members():
    if 'user' in session:
        #conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM Member")
        members = cursor.fetchall()
        member_books = {}
        for member in members:
            member_id = member[0]
            cursor.execute("SELECT bookid FROM book_record WHERE memberid = %s AND isreturned = %s", (member_id, False))
            #cursor.execute("SELECT bookid FROM book_record WHERE id = %s", (member_id,))
            books = cursor.fetchall()
            if books:
                book_ids = [book[0] for book in books]
                cursor.execute("SELECT id, name FROM books WHERE id IN %s", (tuple(book_ids),))
                books_data = cursor.fetchall()
                member_books[member_id] = {'name': member[1], 'books': books_data}
            else:
                member_books[member_id] = {'name': member[1], 'books': []}
        cursor.close()
        #conn.close()
        return render_template('view_members.html', members=members, member_books=member_books)
    else:
        return redirect(url_for('employee_signin'))





@app.route('/view_books')
def view_library_books():
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    cur.close()
    
    return render_template('view_books.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)
