from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__, template_folder='templates')

# Connect to Database
def connect_db():
    conn = sqlite3.connect("books.db")
    conn.row_factory = sqlite3.Row
    return conn

# Initialize Database
def init_db():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT,
        year INTEGER,
        isbn TEXT
    )
    """)
    conn.commit()
    conn.close()

# API Endpoints
@app.route('/books', methods=['GET'])
def get_books():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    conn.close()
    return jsonify([dict(row) for row in books])

@app.route('/search', methods=['GET'])
def search_books():
    title = request.args.get('title', '')
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM books WHERE title LIKE ?", ('%' + title + '%',))
    books = cur.fetchall()
    conn.close()
    return jsonify([dict(row) for row in books])

@app.route('/add', methods=['POST'])
def add_book():
    data = request.json
    title, author, year, isbn = data['title'], data['author'], data['year'], data['isbn']
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO books (title, author, year, isbn) VALUES (?, ?, ?, ?)",
                (title, author, year, isbn))
    conn.commit()
    conn.close()
    return jsonify({"message": "Book added successfully!"}), 201

# Frontend Route
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
