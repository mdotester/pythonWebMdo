from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# Fungsi untuk membuat koneksi ke database
def create_connection():
    connection = pymysql.connect(
        host='172.18.141.41',
        user='administrator',
        password='P@ssw0rd123',
        database='MDO',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

# Endpoint untuk login
@app.route('/bebas', methods=['POST'])
def bebas():
    try:
        bodyReq = request.json
        print(bodyReq)
        name = bodyReq['name']
        email = bodyReq['email']
        pn = bodyReq['pn']
        pw = bodyReq['pw']
        role = bodyReq['role']

        connection = create_connection()
        cursor = connection.cursor()
    
        # Query untuk memeriksa kredensial
        query = "SELECT * FROM MDO_login WHERE name = %s AND email = %s AND pw = %s AND pn = %s AND role = %s"
        cursor.execute(query, (name, email, pw, pn, role))
        
        # # Mendapatkan hasil query
        user = cursor.fetchone()
        # # Menutup koneksi
        cursor.close()
        connection.close()
        
        if user:
        #     # Jika kredensial cocok, kirimkan respons sukses
            return jsonify({'message': 'Login berhasil', 'user': user}), 200
        else:
        #     # Jika kredensial tidak cocok, kirimkan respons gagal
            return jsonify({'message': 'Kredensial tidak valid'}), 401

        # Simpan data pengguna ke database
        # save_user_role(name, email, pw, pn, role)

        # Berikan respons JSON
        return jsonify({"message": "User added successfully"})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Failed to add user"})
    return jsonify(resp)


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    name = data['name']
    email = data['email']
    pn = data['pn']
    pw = data['pw']
    role = data['role']
    
    # Membuat koneksi ke database
    connection = create_connection()
    cursor = connection.cursor()
    
    try:
        # Query untuk memeriksa kredensial
        query = "SELECT * FROM MDO_login WHERE name = %s AND email = %s AND pw = %s AND pn = %s AND role = %s"
        cursor.execute(query, (name, email, pw, pn, role))
        
        # Mendapatkan hasil query
        user = cursor.fetchone()
        
        # Menutup koneksi
        cursor.close()
        connection.close()
        
        if user:
            # Jika kredensial cocok, kirimkan respons sukses
            return jsonify({'message': 'Login berhasil', 'user': user}), 200
        else:
            # Jika kredensial tidak cocok, kirimkan respons gagal
            return jsonify({'message': 'Kredensial tidak valid'}), 401
    except Exception as e:
        # Pesan kesalahan jika terjadi error
        return jsonify({'message': 'Error saat melakukan login: {}'.format(str(e))}), 500

if __name__ == '__main__':
    app.run(debug=True)
