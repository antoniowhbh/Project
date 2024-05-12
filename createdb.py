import sqlite3
from werkzeug.security import generate_password_hash

# Database connection
db_name = 'uniguide_student.db'
connection = sqlite3.connect(db_name)
cursor = connection.cursor()

# Create Students table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students (
        StudentID INTEGER PRIMARY KEY,
        StudentName TEXT NOT NULL,
        Major TEXT NOT NULL,
        Email TEXT NOT NULL
    )
''')

# Create StudentLogins table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS StudentLogins (
        StudentID INTEGER PRIMARY KEY,
        Username TEXT UNIQUE NOT NULL,
        Password TEXT NOT NULL,
        FOREIGN KEY(StudentID) REFERENCES Students(StudentID)
    )
''')

# Create Admins table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Admins (
        AdminID INTEGER PRIMARY KEY,
        AdminName TEXT NOT NULL,
        Username TEXT UNIQUE NOT NULL,
        Password TEXT NOT NULL
    )
''')

# Create AdminActions table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS AdminActions (
        ActionID INTEGER PRIMARY KEY,
        AdminID INTEGER,
        ActionDescription TEXT NOT NULL,
        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(AdminID) REFERENCES Admins(AdminID)
    )
''')

# Create Conversations table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Conversations (
        ConversationID INTEGER PRIMARY KEY,
        StudentID INTEGER,
        Type TEXT NOT NULL CHECK (Type IN ('Regular', 'ChatPDF')),
        ConversationSummary TEXT NOT NULL,
        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        PDFFilePath TEXT,
        FOREIGN KEY(StudentID) REFERENCES Students(StudentID)
    )
''')

# Create Notes table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Notes (
        NoteID INTEGER PRIMARY KEY,
        StudentID INTEGER,
        NoteContent TEXT NOT NULL,
        CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
        AdminID INTEGER,
        FOREIGN KEY(StudentID) REFERENCES Students(StudentID),
        FOREIGN KEY(AdminID) REFERENCES Admins(AdminID)
    )
''')

# Create Classes table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Classes (
        ClassID INTEGER PRIMARY KEY,
        ClassName TEXT NOT NULL,
        ClassDescription TEXT
    )
''')

# Create StudentClasses table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS StudentClasses (
        StudentID INTEGER,
        ClassID INTEGER,
        PRIMARY KEY(StudentID, ClassID),
        FOREIGN KEY(StudentID) REFERENCES Students(StudentID),
        FOREIGN KEY(ClassID) REFERENCES Classes(ClassID)
    )
''')

# Create PDFs table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS PDFs (
        PDFID INTEGER PRIMARY KEY,
        Title TEXT NOT NULL,
        FilePath TEXT NOT NULL,
        UploadedAt DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# Create ChatPDFInteractions table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ChatPDFInteractions (
        InteractionID INTEGER PRIMARY KEY,
        ConversationID INTEGER,
        PDFID INTEGER,
        InteractionDetail TEXT NOT NULL,
        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(ConversationID) REFERENCES Conversations(ConversationID),
        FOREIGN KEY(PDFID) REFERENCES PDFs(PDFID)
    )
''')

# Function to add a fictional student
def add_student(student_name, major, email, username, password):
    cursor.execute(
        "INSERT INTO Students (StudentName, Major, Email) VALUES (?, ?, ?)",
        (student_name, major, email)
    )
    student_id = cursor.lastrowid
    hashed_password = generate_password_hash(password)
    cursor.execute(
        "INSERT INTO StudentLogins (StudentID, Username, Password) VALUES (?, ?, ?)",
        (student_id, username, hashed_password)
    )

# Add fictional students
add_student('Alice Johnson', 'Computer Science', 'alice.johnson@example.com', 'alice_j', 'password123')
# Commit changes and close the connection
connection.commit()
connection.close()
