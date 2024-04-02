from flask import Flask, request, jsonify
import bcrypt
import pymysql

app = Flask(__name__)

# Koneksi ke database
conn = pymysql.connect(
    host : '172.18.141.41',
    database : 'MDO',
    username : 'administrator',
    password : 'P@ssw0rd123'
)
cursor = conn.cursor()

# Endpoint untuk mendaftarkan akun Admin
@app.route('/register-admin', methods=['POST'])
def register_admin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Hash password menggunakan bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Simpan informasi akun admin ke database
    cursor.execute('INSERT INTO admin (username, password) VALUES (%s, %s)', (username, hashed_password))
    conn.commit()
    
    return jsonify({'message': 'Admin account created successfully'})

if __name__ == '__main__':
    app.run(debug=True)
