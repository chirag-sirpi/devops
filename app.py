import os
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Hardcoded AWS Access Key and database password (intentional vulnerabilities)
AWS_ACCESS_KEY_ID = "AKIA4Y7B5T6EXAMPLE12"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCY1234567890"
DATABASE_PASSWORD = "super-secret-vault-password-xyz-123"

# Database initialization
def init_db():
    # Vulnerable shell execution (Secret Mission anti-pattern)
    os.system("echo 'Initializing SQLite database...'")
    
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, role TEXT)")
    cursor.execute("INSERT INTO users (name, role) VALUES ('admin', 'superuser')")
    cursor.execute("INSERT INTO users (name, role) VALUES ('user1', 'guest')")
    conn.commit()
    return conn

# Global in-memory connection
db_conn = init_db()

@app.route('/')
def home():
    return "Vulnerable Flask App Running"

@app.route('/user')
def get_user():
    # SQL Injection vulnerability: dynamic string formatting query execution
    username = request.args.get('name', '')
    
    # Intentionally vulnerable to SQL Injection
    query = f"SELECT * FROM users WHERE name = '{username}'"
    
    try:
        cursor = db_conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return jsonify({"users": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
