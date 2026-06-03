import os
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Read AWS credentials and database password from environment variables (secured)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

# Database initialization
def init_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, role TEXT)")
    cursor.execute("INSERT INTO users (name, role) VALUES ('admin', 'superuser')")
    cursor.execute("INSERT INTO users (name, role) VALUES ('user1', 'guest')")
    conn.commit()
    return conn

# Global database connection
db_conn = init_db()

@app.route('/')
def home():
    return "Vulnerable Flask App Running"

@app.route('/user')
def get_user():
    # Parametrized SQL query: secure against SQL injection
    username = request.args.get('name', '')
    
    query = "SELECT * FROM users WHERE name = ?"
    
    try:
        cursor = db_conn.cursor()
        cursor.execute(query, (username,))
        results = cursor.fetchall()
        return jsonify({"users": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # Bind to localhost (secure)
    app.run(host='127.0.0.1', port=5000)
