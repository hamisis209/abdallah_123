
import os
from flask import Flask, request, jsonify, render_template_string
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# PostgreSQL connection settings (update with your credentials)
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'nhm_db')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASS = os.environ.get('DB_PASS', 'password')

# Connect to PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        cursor_factory=RealDictCursor
    )

@app.route('/')
def home():
    return 'Flask backend is running!'

@app.route('/api/register', methods=['POST'])
    data = request.json
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        hashed_password = generate_password_hash(data['password'])
        cur.execute('''INSERT INTO users (username, password, phone) VALUES (%s, %s, %s)''',
                    (data['username'], hashed_password, data.get('phone')))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'status': 'success'}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/login', methods=['POST'])
    data = request.json
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username=%s', (data['username'],))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user and check_password_hash(user['password'], data['password']):
            # Remove password from response for security
            user.pop('password', None)
            return jsonify({'status': 'success', 'user': user}), 200
        else:
            return jsonify({'status': 'fail', 'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/recover', methods=['POST'])
def recover():
    data = request.json
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username=%s', (data['username'],))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            # In a real app, send email here
            return jsonify({'status': 'success', 'message': 'Recovery instructions sent.'}), 200
        else:
            return jsonify({'status': 'fail', 'message': 'User not found.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
