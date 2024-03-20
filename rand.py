import random
import hashlib
from passlib.hash import sha256_crypt
import psycopg2

# Function to generate fake names
def generate_fake_name():
    first_names = ['Emma', 'Keanu', 'Viola']
    last_names = ['Stone', 'Reeves', 'Davis']
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# Function to generate fake email addresses
def generate_fake_email():
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'example.com']
    return f"{generate_fake_name().replace(' ', '.').lower()}@{random.choice(domains)}"

# Function to generate fake passwords and hash them using sha256_crypt
def generate_fake_password():
    password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()', k=10))
    return sha256_crypt.encrypt(password)


# Function to generate fake contact numbers
def generate_fake_contact():
    return ''.join(random.choices('0123456789', k=8))

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="library",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Generate SQL code to populate the table
sql_insert = "INSERT INTO employee (name, email, password, contact) VALUES\n"
for i in range(3):
    name = generate_fake_name()
    email = generate_fake_email()
    password = generate_fake_password()
    contact = generate_fake_contact()
    sql_insert += f"('{name}', '{email}', '{password}', '{contact}')"
    if i < 2:
        sql_insert += ",\n"
    else:
        sql_insert += ";\n"

# Execute SQL code
cursor.execute(sql_insert)
conn.commit()

# Close connection
cursor.close()
conn.close()

print("Table populated successfully.")
