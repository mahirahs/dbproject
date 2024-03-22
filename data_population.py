'''import random
import psycopg2

# Function to generate fake names
def generate_fake_name():
    words = ["book", "chair", "table", "lamp", "computer",
    "pen", "pencil", "notebook", "backpack", "clock",
    "door", "window", "car", "bicycle", "phone",
    "keyboard", "mouse", "monitor", "desk", "calendar",
    "guitar", "television", "headphones", "speaker", "microphone",
    "camera", "mirror", "wallet", "umbrella", "shoe",
    "sock", "shirt", "pants", "hat", "glasses",
    "scarf", "glove", "jacket", "tie", "belt",
    "bracelet", "ring", "watch", "necklace", "earrings",
    "suitcase", "brush", "comb", "perfume", "lotion", "run", "jump", "swim", "climb", "fly",
    "read", "write", "sing", "dance", "draw",
    "paint", "cook", "bake", "drive", "walk",
    "talk", "listen", "laugh", "cry", "sleep",
    "eat", "drink", "think", "learn", "teach",
    "play", "work", "clean", "wash", "brush",
    "kick", "throw", "catch", "build", "fix",
    "open", "close", "move", "lift", "push",
    "pull", "cut", "slice", "chop", "mix",
    "stir", "pour", "shake", "breathe", "smile"]
    num_words = random.randint(2, 3)
    name = ' '.join(random.choice(words) for _ in range(num_words))
    return name.capitalize()

# Function to generate fake author names
def generate_fake_author():
    first_names = ['John', 'James', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph', 'Thomas', 'Charles', "Liam", "Olivia", "Noah", "Emma", "Oliver",
    "Ava", "William", "Sophia", "Elijah", "Isabella",
    "James", "Mia", "Benjamin", "Charlotte", "Lucas",
    "Amelia", "Henry", "Harper", "Alexander", "Evelyn",
    "Michael", "Abigail", "Ethan", "Emily", "Daniel",
    "Elizabeth", "Matthew", "Sofia", "Jackson", "Avery",
    "David", "Ella", "Joseph", "Madison", "Logan",
    "Scarlett", "Samuel", "Victoria", "Sebastian", "Grace",
    "Carter", "Chloe", "Gabriel", "Lily", "Owen",
    "Hannah", "John", "Lillian", "Dylan", "Nora"]
    last_names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor', "Smith", "Johnson", "Williams", "Jones", "Brown",
    "Davis", "Miller", "Wilson", "Moore", "Taylor",
    "Anderson", "Thomas", "Jackson", "White", "Harris",
    "Martin", "Thompson", "Garcia", "Martinez", "Robinson",
    "Clark", "Rodriguez", "Lewis", "Lee", "Walker",
    "Hall", "Allen", "Young", "Hernandez", "King",
    "Wright", "Lopez", "Hill", "Scott", "Green",
    "Adams", "Baker", "Gonzalez", "Nelson", "Carter",
    "Mitchell", "Perez", "Roberts", "Turner", "Phillips",
    "Campbell", "Parker", "Evans", "Edwards", "Collins"]
    author = ' '.join([random.choice(first_names), random.choice(last_names)])
    return author

# Function to generate fake publisher names
def generate_fake_publisher():
    words = ['Penguin', 'Random', 'HarperCollins', 'Simon', 'Schuster', 'Macmillan', 'Hachette', 'Bloomsbury', 'Oxford', 'Cambridge']
    return random.choice(words)

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
sql_insert = "INSERT INTO books (name, author, publisher, status) VALUES\n"
for i in range(1500):
    name = generate_fake_name()
    author = generate_fake_author()
    publisher = generate_fake_publisher()
    sql_insert += f"('{name}', '{author}', '{publisher}', 'available')"
    if i < 1499:
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
'''
'''
import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="library",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Retrieve distinct authors from the Books table
cursor.execute("SELECT DISTINCT author FROM books;")
authors = cursor.fetchall()

# Insert authors into the Authors table sequentially
for author in authors:
    author_name = author[0]
    cursor.execute("INSERT INTO author (name) VALUES (%s);", (author_name,))
    conn.commit()

# Close connection
cursor.close()
conn.close()

print("Authors inserted into Authors table successfully.")
'''
'''
import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="library",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Retrieve distinct publishers from the Books table
cursor.execute("SELECT DISTINCT publisher FROM books;")
publishers = cursor.fetchall()

# Insert publishers into the Publisher table sequentially
for publisher in publishers:
    publisher_name = publisher[0]
    cursor.execute("INSERT INTO publisher (name) VALUES (%s);", (publisher_name,))
    conn.commit()

# Close connection
cursor.close()
conn.close()

print("Publishers inserted into Publisher table successfully.")
'''


import random
import hashlib
from passlib.hash import sha256_crypt
import psycopg2

# Function to generate fake names
def generate_fake_name():
    first_names = ["Ethan", "Aria", "Mason", "Aurora", "Logan",
    "Zoe", "Evan", "Harmony", "Landon", "Natalie",
    "Caleb", "Luna", "Ryan", "Stella", "Connor",
    "Willow", "Isaac", "Nova", "Blake", "Hazel",
    "Nathan", "Piper", "Dylan", "Ivy", "Wyatt",
    "Savannah", "Luke", "Penelope", "Christopher", "Ruby",
    "Isaiah", "Serenity", "Aaron", "Autumn", "Jack",
    "Bella", "Tyler", "Aaliyah", "Christian", "Layla",
    "Adrian", "Violet", "Brayden", "Elena", "Julian",
    "Aubrey", "Nicholas", "Quinn", "Dominic", "Katherine"]
    last_names = ["Cooper", "Rossi", "Richardson", "Khan", "Hughes",
    "Stewart", "Murray", "Fisher", "Cox", "Bishop",
    "Rose", "Barnes", "West", "Holland", "Webb",
    "May", "Harrison", "Gibson", "Pearson", "Graham",
    "Arnold", "Barrett", "Wade", "Hudson", "Dixon",
    "Harper", "Holmes", "Palmer", "Jordan", "Francis",
    "Reid", "Perry", "Hawkins", "Grant", "Mills",
    "Fleming", "Owen", "Kennedy", "Wells", "Coleman",
    "Fuller", "Greene", "Stanley", "Chambers", "Bates",
    "Morton", "Lawrence", "Jacobs", "Fowler", "Horton"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# Function to generate fake email addresses
'''
def generate_fake_email():
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'example.com']
    return f"{generate_fake_name().replace(' ', '.').lower()}@{random.choice(domains)}"
'''
'''
# Function to generate fake email addresses
def generate_fake_email(cursor):
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'example.com']
    while True:
        email = f"{generate_fake_name().replace(' ', '.').lower()}@{random.choice(domains)}"
        cursor.execute("SELECT COUNT(*) FROM Member WHERE email = %s", (email,))
        if cursor.fetchone()[0] == 0:
            return email


# Function to generate fake passwords and hash them using sha256_crypt
def generate_fake_password():
    password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()', k=10))
    return sha256_crypt.encrypt(password)

# Function to generate fake member types
def generate_fake_member_type():
    return random.choice(['student', 'teacher'])

# Function to generate fake contact numbers
def generate_fake_contact():
    return ''.join(random.choices('0123456789', k=10))

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
sql_insert = "INSERT INTO Member (name, email, password, member_type, contact, fine) VALUES\n"
for i in range(200):
    name = generate_fake_name()
    email = generate_fake_email(cursor)
    password = generate_fake_password()
    member_type = generate_fake_member_type()
    contact = generate_fake_contact()
    sql_insert += f"('{name}', '{email}', '{password}', '{member_type}', '{contact}', 0)"
    if i < 199:
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
'''
'''
import random
import hashlib
from passlib.hash import sha256_crypt
import psycopg2

# Function to generate fake names
def generate_fake_name():
    first_names = ["Ethan", "Aria", "Mason", "Aurora", "Logan",
    "Zoe", "Evan", "Harmony", "Landon", "Natalie",
    "Caleb", "Luna", "Ryan", "Stella", "Connor",
    "Willow", "Isaac", "Nova", "Blake", "Hazel",
    "Nathan", "Piper", "Dylan", "Ivy", "Wyatt",
    "Savannah", "Luke", "Penelope", "Christopher", "Ruby",
    "Isaiah", "Serenity", "Aaron", "Autumn", "Jack",
    "Bella", "Tyler", "Aaliyah", "Christian", "Layla",
    "Adrian", "Violet", "Brayden", "Elena", "Julian",
    "Aubrey", "Nicholas", "Quinn", "Dominic", "Katherine"]
    last_names = ["Cooper", "Rossi", "Richardson", "Khan", "Hughes",
    "Stewart", "Murray", "Fisher", "Cox", "Bishop",
    "Rose", "Barnes", "West", "Holland", "Webb",
    "May", "Harrison", "Gibson", "Pearson", "Graham",
    "Arnold", "Barrett", "Wade", "Hudson", "Dixon",
    "Harper", "Holmes", "Palmer", "Jordan", "Francis",
    "Reid", "Perry", "Hawkins", "Grant", "Mills",
    "Fleming", "Owen", "Kennedy", "Wells", "Coleman",
    "Fuller", "Greene", "Stanley", "Chambers", "Bates",
    "Morton", "Lawrence", "Jacobs", "Fowler", "Horton"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# Function to generate fake email addresses
def generate_fake_email():
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'example.com']
    return f"{generate_fake_name().replace(' ', '.').lower()}@{random.choice(domains)}"

# Function to generate fake passwords and hash them using sha256_crypt
def generate_fake_password():
    password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()', k=10))
    return sha256_crypt.encrypt(password)

# Function to generate fake member types
def generate_fake_member_type():
    return random.choice(['student', 'teacher'])

# Function to generate fake contact numbers
def generate_fake_contact():
    return ''.join(random.choices('0123456789', k=10))

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
sql_insert = "INSERT INTO Member (name, email, password, member_type, contact, fine) VALUES\n"
emails_set = set()
for i in range(200):
    name = generate_fake_name()
    email = generate_fake_email()
    # Ensure email uniqueness
    while email in emails_set:
        email = generate_fake_email()
    emails_set.add(email)
    password = generate_fake_password()
    member_type = generate_fake_member_type()
    contact = generate_fake_contact()
    sql_insert += f"('{name}', '{email}', '{password}', '{member_type}', '{contact}', 0)"
    if i < 199:
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
'''

import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="library",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Alter the sequence to start from 1
cursor.execute("ALTER SEQUENCE member_id_seq RESTART WITH 1;")

# Commit the transaction
conn.commit()

# Close connection
cursor.close()
conn.close()

print("Sequence altered successfully.")