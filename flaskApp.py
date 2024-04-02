from flask import Flask,request,jsonify
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
import myLogger
import requests
import pandas as pd
import databaseMySql as db
import mysql.connector
from flask_cors import CORS
import paramiko
import os
import sqlite3 as sql
import pymysql



USER_DATA = {
    "admin": {"password": "SuperSecretPwd", "role": "admin"},
    "maker": {"password": "MakerPwd", "role": "maker"},
    "checker": {"password": "CheckerPwd", "role": "checker"},
    "signer": {"password": "SignerPwd", "role": "signer"},
}

app = Flask(__name__)
CORS(app)

auth = HTTPBasicAuth()

# CORS(app)  # Untuk mengaktifkan CORS agar frontend dapat berkomunikasi dengan backend
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     privilege = db.Column(db.String(50), nullable=False)

#     def __repr__(self):
#         return f"<User {self.username}>"

# # Endpoint untuk menambahkan pengguna baru
# @app.route('/add_user', methods=['POST'])
# def add_user():
#     data = request.json
#     username = data.get('username')
#     email = data.get('email')

#     if not username or not email:
#         return jsonify({'message': 'Incomplete data'}), 400

#     new_user = User(email=email, password=password)
#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({'message': 'User added successfully'}), 201

# # Endpoint untuk mendapatkan daftar pengguna
# @app.route('/user', methods=['GET'])
# def get_users():
#     users = User.query.all()
#     user_list = [{'username': user.username, 'email': user.email, 'privilege': user.privilege} for user in users]
#     return jsonify(user_list), 200


dbMDO = {
    'host' : "172.18.141.41",
    'database' : 'MDO',
    'username' : 'administrator',
    'password' : 'P@ssw0rd123'
}



dbDEV = {
    'host' : "127.0.0.1",
    'database' : 'MDO',
    'username' : 'sa',
    'password' : 'P@ssw0rd'
}


# KONFIGURASI ANSIBLE
#AWX_IP = "172.18.53.100"
#AWX_TOKEN = "crGU7ZVYLkMjpXPq30L2LlQjdKVkqd"
#JOB_TEMPLATE_ID = 36  # Ganti dengan ID templat pekerjaan yang ingin Anda jalankan
#HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {AWX_TOKEN}"}
#url = "http://172.18.53.100"

#import os
#no_proxy_hosts = ["localhost", "127.0.0.1", "172.18.53.100"]
#os.environ["no_proxy"] = ",".join(no_proxy_hosts)
#responseAnsible = requests.get(url)
#print(responseAnsible.text)


#KONFIGURASI REMOVE 
hostname = '2.0.0.217'
port = 22
username = 'pswaix'
password = 'pswaix'

# Direktori dan nama file lokal
local_dir1 = '/home/projects/irwin/project_web/Backend/pythonWebMdo/'
local_dir2 = '/home/projects/irwin/project_web/Backend/pythonWebMdo/'
local_file1 = 'conn-down2.p'
local_file2 = 'conndown2.sh'

# Direktori tujuan di server
remote_dir1 = '/u/pswaix/psw/1a/main/'
remote_dir2 = '/u/pswaix/psw/1a/bin/'

#KONFIGURASI LOGON

local_dir3 = '/home/projects/irwin/project_web/Backend/pythonWebMdo/'
local_dir4 = '/home/projects/irwin/project_web/Backend/pythonWebMdo/'
local_file3 = 'conn-up2.p'
local_file4 = 'connup2.sh'

# Direktori tujuan di server
remote_dir3 = '/u/pswaix/psw/1a/main/'
remote_dir4 = '/u/pswaix/psw/1a/bin/'



#@auth.verify_password
#def verify(username, password):
#    if not (username and password):
 #       return False
#    return USER_DATA.get(username) == password

@app.route('/grafanaNotify/', methods=['POST'])
# @auth.login_required
def grafanaNotify():
    resp = {'status':False}
    body = request.json
    myLogger.logging_info('flask','/grafanaNotify/ \t','body:',body,'\t')

    response = jsonify(resp)
    return response

#@auth.login_required
#def login prod
# def login():
#     resp = {'status':False}
#     body = request.json
#     try:
#         url = 'https://apiclose.bri.co.id/gateway/apiActiveDirectory/1.0/ADAuthentication2'
#         headers = {"Authorization":"Basic Y29udGFjdENlbnRlcjpDMG50NGN0QzNudGVyITE0MDE3","Content-Type":"application/json"}
#         myLogger.logging_info('flask','/login/ \t','body:',body,'\t')
#         # json = body
#         response = requests.post(url,headers=headers,json = body)
#         jsonResp = response.json()
#         myLogger.logging_info('flask','/ADAuthentication2/ \t','jsonResp:',jsonResp,'\t')
#         if jsonResp['responseCode'] == '00':
#             #inquiry pn detail
#             resp['status'] = True
#             url = 'https://apiclose.bri.co.id/gateway/apiBristars/1.0/pekerja/inquiryPekerjaByPn'
#             headers = {"Authorization":"Basic Y29udGFjdENlbnRlcjpDMG50NGN0QzNudGVyITE0MDE3","Content-Type":"application/json"}
#             response_detail_pn = requests.post(url,headers=headers,json = {'pernr':body['userLogin']})
#             json_response_detail_pn = response_detail_pn.json()
#             myLogger.logging_info('flask','/inquiryPekerjaByPn/ \t','jsonResp:',json_response_detail_pn,'\t')
#             resp['data'] = json_response_detail_pn['responseData']
#             resp['data']['email'] = jsonResp['responseMessage']
#         else :
#             resp['message'] = 'Invalid Credentials'
#         myLogger.logging_info('flask','/login/ \t','response:',response.json(),'\t')
#     except Exception as e:
#         myLogger.logging_error('flask','got error login,e:',e)
#     return jsonify(resp)

def save_registration_data(username, email, password, pn, role):
    try:
        # Buat koneksi ke database
        connection = pymysql.connect(host=dbMDO['host'],
                                     user=dbMDO['username'],
                                     password=dbMDO['password'],
                                     database=dbMDO['database'],
                                     cursorclass=pymysql.cursors.DictCursor)
        
        # Jalankan perintah SQL untuk menyimpan data
        with connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO users (username, email, password, pn, role) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (username, email, password, pn, role))
                connection.commit()
    except Exception as e:
        print("Failed to save registration data:", str(e))

# Endpoint untuk registrasi pengguna
@app.route('/register', methods=['POST'])
def register():
    try:
        # Ambil data dari request JSON
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        pn = data.get('pn')
        role = data.get('role')

        # Validasi data
        if not username or not email or not password or not pn or not role:
            return jsonify({'message': 'All fields are required'}), 400

        # Simpan data registrasi ke database
        save_registration_data(username, email, password, pn, role)

        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'message': 'Failed to register user', 'error': str(e)}), 500
        
#def login dev
@app.route('/login/', methods=['POST'])
def login():
    resp = {'status': False}
    body = request.json
    try:
        # Autentikasi
        url_auth = 'https://apiclose.bri.co.id/gateway/apiActiveDirectory/1.0/ADAuthentication2'
        headers_auth = {"Authorization": "Basic Y29udGFjdENlbnRlcjpDMG50NGN0QzNudGVyITE0MDE3", "Content-Type": "application/json"}
        response_auth = requests.post(url_auth, headers=headers_auth, json=body)
        response_auth_data = response_auth.json()
        myLogger.logging_info('flask', '/login/ \t', 'response_auth:', response_auth_data, '\t')
        
        # Periksa autentikasi sukses
        if response_auth.status_code == 200 and response_auth_data.get('responseCode') == '00':
            # Permintaan detail PN
            url_pn = 'https://apiclose.bri.co.id/gateway/apiBristars/1.0/pekerja/inquiryPekerjaByPn'
            headers_pn = {"Authorization": "Basic Y29udGFjdENlbnRlcjpDMG50NGN0QzNudGVyITE0MDE3", "Content-Type": "application/json"}
            response_detail_pn = requests.post(url_pn, headers=headers_pn, json={'pernr': body['userLogin']})
            json_response_detail_pn = response_detail_pn.json()
            myLogger.logging_info('flask', '/inquiryPekerjaByPn/ \t', 'response_detail_pn:', json_response_detail_pn, '\t')

            # Periksa response detail PN
            if response_detail_pn.status_code == 200 and 'responseData' in json_response_detail_pn:
                # Periksa nilai "orgehTX"
                if json_response_detail_pn['responseData'].get('orgehTX') == 'MIDDLEWARE APPLICATION OPERATION SERVICES FUNCTION':
                    resp['status'] = True
                    resp['data'] = json_response_detail_pn['responseData']
                    resp['data']['email'] = response_auth_data['responseMessage']
                    
                    # Define login_berhasil as True when authentication and PN detail checks are successful
                    login_berhasil = True
                    
                    # Simpan record ke database
                    save_login_record(userLogin=body['userLogin'], email=response_auth_data['responseMessage'], orgehTX='MIDDLEWARE APPLICATION OPERATION SERVICES FUNCTION')
                else:
                    resp['message'] = 'User Tidak Terdaftar'
            else:
                resp['message'] = 'PN dan Password Salah'
        else:
            resp['message'] = 'PN dan Password Salah'
            
        myLogger.logging_info('flask', '/login/ \t', 'response:', response_auth_data, '\t')
    except Exception as e:
        myLogger.logging_error('flask', 'got error login, e:', e)
        resp['message'] = 'Error occurred during login process'

    return jsonify(resp)

def save_login_record(userLogin, email, orgehTX):
   try:
       connection = pymysql.connect(host=dbMDO['host'],
                                    user=dbMDO['username'],
                                    password=dbMDO['password'],
                                    database=dbMDO['database'],
                                    cursorclass=pymysql.cursors.DictCursor)
        
       with connection:
           with connection.cursor() as cursor:
               sql = "INSERT INTO LoginRecords (userLogin, email, orgehTX) VALUES (%s, %s, %s)"
               cursor.execute(sql, (userLogin, email, orgehTX))
               connection.commit()
   except Exception as e:
       print("Failed to save login record:", str(e))

@app.route("/userManage/", methods=['POST'])
def usermanage():
    try:
        bodyReq = request.json
        nm = bodyReq['name']
        pn = bodyReq['pn']
        pw = bodyReq['password']
        role = bodyReq['role']

        # Simpan data pengguna ke database
        save_user_role(nm, pn, pw, role)

        # Berikan respons JSON
        return jsonify({"message": "User added successfully"})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Failed to add user"})
    return jsonify(resp)

def save_user_role(name, pn, password, role):
    try:
        connection = pymysql.connect(host=dbMDO['host'],
                                     user=dbMDO['username'],
                                     password=dbMDO['password'],
                                     database=dbMDO['database'],
                                     cursorclass=pymysql.cursors.DictCursor)
        
        with connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO UserManage (name, pn, password, role) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (name, pn, password, role))
                connection.commit()
    except Exception as e:
        print("Failed to save user", str(e))

# @app.route('/adduser/', methods=['POST'])
# def adduser():
#         print("Entered")
#         try:
#             personalnum = bodyReq['personalnum']
#             password = bodyReq['password']
#             role = bodyReq['role']
#             print(personalnum, password, role)
#             VALUE("INSERT INTO MDO_app (personalnum, password, role) VALUES (%s, %s, %s)", (personalnum, password, role))        
#             print("Registered")
#         except Exception as e:
#             return str(e)

# def add_data(personalnum, password, role):  
#   try:
#     # Connecting to database
#     con = sql.connect('172.18.141.41')
#     # Getting cursor
#     c =  con.cursor() 
#     # Adding data
#     c.execute("INSERT INTO MDO_app (personalnum, password, role) VALUES (%s, %s, %s)" %(personalnum, password, role))
#     # Applying changes
#     con.commit() 
#   except:
#     print("An error has occured")

@app.route('/fetchService/', methods=['POST'])
@auth.login_required
def fetchService():
    resp = {'status':False, 'exist':True}
    # body = request.json
    body = "sEcho=1&iColumns=9&sColumns=%2C%2C%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=10&mDataProp_0=service_id&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=aggregator_id&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=true&mDataProp_2=trx_type_id&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=limit_type_id&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=esb_svc_name&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=true&mDataProp_5=advance_svc_name&sSearch_5=&bRegex_5=false&bSearchable_5=true&bSortable_5=true&mDataProp_6=service_desc&sSearch_6=&bRegex_6=false&bSearchable_6=true&bSortable_6=true&mDataProp_7=is_conditional_fee&sSearch_7=&bRegex_7=false&bSearchable_7=true&bSortable_7=true&mDataProp_8=service_id&sSearch_8=&bRegex_8=false&bSearchable_8=false&bSortable_8=false&sSearch=&bRegex=false&iSortCol_0=0&sSortDir_0=asc&iSortingCols=1"
    try:
        url = 'http://172.18.39.117:8080/bridashboard/fetchService'
        headers = {
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7",
            "Access-Control-Allow-Credentials": "*",
            "Content-Length": "943",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Connection": "keep-alive",
            "Cookie": "JSESSIONID=2F8D9C47B79C7D98DF59CEDC7BE09C52",
            "Host": "172.18.39.118:8080",
            "Origin": "http://172.18.39.117:8080",
            "Referer": "http://172.18.39.117:8080/bridashboard/listService"
        }
        myLogger.logging_info('flask','/fetchService/ \t','body:',body,'\t')
        # json = body
        response = requests.post(url,headers=headers,data = body)
        jsonResp = response.json()
        myLogger.logging_info('flask','/fetchService - Response/ \t','jsonResp:',jsonResp,'\t')
        # myLogger.logging_info('flask','/listService/ \t','response:',response.text,'\t')
        if jsonResp['sEcho'] == 1:
            resp['status'] = True
            resp['data'] = jsonResp['data']
            resp['count'] = jsonResp['iTotalRecords']
        else :
            resp['message'] = 'Invalid Credentials'
        # myLogger.logging_info('flask','/fetchService/ \t','response:',response.json(),'\t')
    except Exception as e:
        myLogger.logging_error('flask','got error fetch,e:',e)
    return jsonify(resp)

@app.route('/updateCacheESB/', methods=['POST'])
@auth.login_required
def updateCacheESB():
    resp = {'status':False}
    try:
        body = request.json
        myLogger.logging_info('flask','/updateCacheESB/ \t','body:',body,'\t')
        sql = selectQueryUpdateCacheESB(body)
        mapRowsSelected = {'IP':0,'ESBType':1,'PortIs':2,'Site':3,'Authorization':4}
        if sql != '':
            svcName = body['svcName']
            data = []
            rows = db.selectData(sql,dbMDO)
            for row in rows:
                try:
                    url = 'http://' + row[mapRowsSelected['IP']] + ':' + row[mapRowsSelected['PortIs']] +'/invoke/' + svcName
                    headers = {"Authorization":row[mapRowsSelected['Authorization']],"Content-Type":"application/json"}
                    response = requests.get(url,headers=headers)
                    if response.status_code == 200 :
                        data.append({'IP':row[mapRowsSelected['IP']],'Status':'success : ' + str(response.status_code)})
                        # data[row[mapRowsSelected['IP']]] = 'success : ' + str(response.status_code)
                    else :
                        data.append({'IP':row[mapRowsSelected['IP']],'Status':'fail : ' + str(response.status_code)})
                        # data[row[mapRowsSelected['IP']]] = 'fail :' + str(response.status_code)
                except Exception as e:
                    myLogger.logging_error('flask',' got except when hit ',row[mapRowsSelected['IP']], ',e:',e)
                    data[row[mapRowsSelected['IP']]] = 999
            resp['data'] = data
            resp['status'] = True
        else :
            resp['message'] = 'fail to generate query'
    except Exception as e:
        myLogger.logging_error('flask','got error updateCacheESB, e:',e)
    return jsonify(resp)

@app.route('/createAlert/', methods=['POST'])
@auth.login_required
def createAlert():
    resp = {'status':False}
    try:
        body = request.json
        myLogger.logging_info('flask','/createAlert/ \t','body:',body,'\t')
        strSql = insertQueryAlert(body)
        if strSql != '':
            result = db.executeQuery(strSql, dbMDO)
            resp['result'] = 'Pengingat' + body['name'] + 'berhasil ditambahkan'
            resp['status'] = True
        else :
            resp['message'] = 'fail to generate query'
    except Exception as e:
        myLogger.logging_error('flask','got error createAlert, e:',e)
    return jsonify(resp)

def insertQueryAlert(bodyReq):
    alertName = bodyReq['alertName']
    groupName = bodyReq['groupName']
    caption = bodyReq['caption']
    kibanaQuery = bodyReq['kibanaQuery']
    threshold = bodyReq['threshold']

    sql = f"INSERT INTO alert (name, kql_query, threshold, group_name_wa, caption) \
    VALUE(\'{alertName}\',\'{kibanaQuery}\',\'{threshold}\', \'{groupName}\',\'{caption}\' );"
    return sql

# Intended for development purpose, for querying from BRI_SERVICE_DUMMY ON 141.41
@app.route('/esbGet/', methods=['GET'])
# @auth.login_required
def getEsbData():
    resp = {'status':False}
    sql = ' SELECT * FROM BRI_SERVICE_DUMMY LIMIT 150; '
    mapRowsSelected = {
        'SERVICE_ID':0,
        'AGGREGATOR_ID':1,
        'TRX_TYPE_ID':2,
        'LIMIT_TYPE_ID':3,
        'ESB_SVC_NAME':4,
        'ADVANCE_SVC_NAME':5,
        'SERVICE_DESC':6,
        'IS_CONDITIONAL_FEE':7,
        'EXISTING_REMARK_FORMULA':8,
        'EXISTING_REMARK2_FORMULA':9,
        'DO_FRAUD_CHECK':10
        }
    if sql != '':
        data = []
        #prod
        rows = db.selectData(sql,dbMDO)
        
        #dev
        #rows = db.selectData(sql,dbDEV)
        for row in rows:
            try:
                data.append({
                    'SERVICE_ID':row[mapRowsSelected['SERVICE_ID']],
                    'AGGREGATOR_ID':row[mapRowsSelected['AGGREGATOR_ID']],
                    'TRX_TYPE_ID':row[mapRowsSelected['TRX_TYPE_ID']],
                    'LIMIT_TYPE_ID':row[mapRowsSelected['LIMIT_TYPE_ID']],
                    'ESB_SVC_NAME':row[mapRowsSelected['ESB_SVC_NAME']],
                    'ADVANCE_SVC_NAME':row[mapRowsSelected['ADVANCE_SVC_NAME']],
                    'SERVICE_DESC':row[mapRowsSelected['SERVICE_DESC']],
                    'IS_CONDITIONAL_FEE':row[mapRowsSelected['IS_CONDITIONAL_FEE']],
                    'EXISTING_REMARK_FORMULA':row[mapRowsSelected['EXISTING_REMARK_FORMULA']],
                    'EXISTING_REMARK2_FORMULA':row[mapRowsSelected['EXISTING_REMARK2_FORMULA']],
                    'DO_FRAUD_CHECK':row[mapRowsSelected['DO_FRAUD_CHECK']]
                    })
            except Exception as e:
                myLogger.logging_error('flask', 'error getEsb, e:', e)
        resp['data'] = data
        resp['status'] = True
    else : 
        resp['message'] = 'fail to generate query'
    return jsonify(resp)

# Intended for development purpose, for disabling service from BRI_SERVICE_DUMMY ON 141.41
@app.route('/esbDisable/<serviceId>', methods=['POST'])
@auth.login_required
def esbDisable(serviceId):
    resp = {'status':False}
    #Change first letter of SERVICE_ID to 'Z'
    updatedServiceId = 'Z' + serviceId[1:]
    #Insert updated service id to BRI_SERVICE_DUMMY
    sql = 'UPDATE BRI_SERVICE_DUMMY SET SERVICE_ID = \'' + updatedServiceId +  '\' WHERE SERVICE_ID = \'' + serviceId + '\';'
    #Insert updated history of updated service into BRI_SERVICE_HISTORY
    sqlInsertHist = 'INSERT INTO BRI_SERVICE_HISTORY (OLD_SERVICE_ID,UPDATED_SERVICE_ID,STATUS) VALUES (\'' + serviceId + '\',\'' + updatedServiceId + '\',\'DISABLED\');'
    try:
        #prod
        result = db.executeQuery(sql, dbMDO)
        insertHistoryStatus = db.executeQuery(sqlInsertHist, dbMDO)

        #dev
        #result = db.executeQuery(sql, dbDEV)
        #insertHistoryStatus = db.executeQuery(sqlInsertHist, dbDEV)
        
        resp['insertHistoryStatus'] = insertHistoryStatus
        resp['result'] = result
        resp['status'] = True
    except Exception as e:
        myLogger.logging_error('flask', 'disable service failed (esbDisable), e:',e)
    return jsonify(resp)

# Intended for development purpose, for enabling service from BRI_SERVICE_DUMMY ON 141.41
# Untuk yang enable ini sudah bisa, cuma kurang untuk delete data di tabel history ---> DONE
# Next -> Apakah perlu untuk delete data di tabel history? Atau dibiarkan saja sebagai log perubahan.
@app.route('/esbEnable/<serviceId>', methods=['POST'])
@auth.login_required
def esbEnable(serviceId):
    resp = {'status' : False}
    resp['serviceID'] = serviceId
    sqlSelectHist = 'SELECT * FROM BRI_SERVICE_HISTORY WHERE UPDATED_SERVICE_ID = Z\'' + serviceId + '\';'
    mapRowsSelected = {
        'OLD_SERVICE_ID':0,
        'UPDATED_SERVICE_ID':1,
        'STATUS':2
    }
    try:
        data = []
        #prod
        rows = db.selectData(sqlSelectHist,dbMDO)
        
        #dev
        #rows = db.selectData(sqlSelectHist,dbDEV)
        for row in rows:
            # resp['result'] = result
            try:
                data.append({
                    'OLD_SERVICE_ID':row[mapRowsSelected['OLD_SERVICE_ID']],
                    'UPDATED_SERVICE_ID':row[mapRowsSelected['UPDATED_SERVICE_ID']],
                    'STATUS':row[mapRowsSelected['STATUS']]
                    })
            except Exception as e:
                myLogger.logging_error('flask', 'enable service failed (esbEnable), e:',e)
        # resp['data']=data
        oldServiceId = data[0]['OLD_SERVICE_ID']
        updatedServiceId = data[0]['UPDATED_SERVICE_ID']
        resp['oldService'] = oldServiceId
        resp['updatedServiceId'] = updatedServiceId

        sql = 'UPDATE BRI_SERVICE_DUMMY SET SERVICE_ID = \'' + oldServiceId +  '\' WHERE SERVICE_ID = \'' + updatedServiceId + '\';'
        sqlDeleteHist = 'DELETE FROM BRI_SERVICE_HISTORY WHERE UPDATED_SERVICE_ID = \'' + updatedServiceId + '\';'
        try:
            #prod
            result = db.executeQuery(sql,dbMDO)
            deleteStatus = db.executeQuery(sqlDeleteHist, dbMDO)

            #dev
            #result = db.executeQuery(sql,dbDEV)
            #deleteStatus = db.executeQuery(sqlDeleteHist, dbDEV)

            resp['result'] = result
            resp['deleteStatus'] = deleteStatus
            resp['status'] = True
        except Exception as e:
            myLogger.logging_error('flask', 'enable service failed (esbEnable), e:',e)    

    except Exception as e:
        myLogger.logging_error('flask', 'enable service failed (esbEnable), e:',e)

    return jsonify(resp)

@app.route('/api/user/database', methods=['POST'])
def set_user_database():
    data = request.json  # Mendapatkan data koneksi dari permintaan JSON
    user_id = data.get('id_user')
    nama = data.get('nama')
    email = data.get('email')
    password = data.get('password')

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Simpan detail koneksi database dalam tabel pengguna
    user.user_id = id_user
    user.nama = nama
    user.email = email
    user.password = password
    db.session.commit()


@app.route('/audit/', methods=['POST'])
@auth.login_required
def auditInsert():
    resp = {'status':False}
    try:
        body = request.json
        myLogger.logging_info('flask','Audit Insert Body \t','body:',body,'\t')

        TIMESTAMP = body['TIMESTAMP']
        PN = body['PN']
        NAME = body['NAME']
        TYPE = body['TYPE']
        MESSAGE = body['MESSAGE']
        strSql = f"INSERT INTO AUDIT_TRAIL (TIMESTAMP, PN, NAME, TYPE, MESSAGE) \
        VALUE(\'{TIMESTAMP}\',\'{PN}\',\'{NAME}\', \'{TYPE}\',\'{MESSAGE}\' );"

        if strSql != '':
            #Prod
            result = db.executeQuery(strSql, dbMDO)

            #Dev
            #result = db.executeQuery(strSql, dbDEV)
            # resp['result'] = 'Pengingat' + body['name'] + 'berhasil ditambahkan'
            resp['result'] = "Success adding audit"
            resp['status'] = True
        else :
            resp['message'] = 'fail to generate query'
    except Exception as e:
        myLogger.logging_error('flask','Error while inserting audit, e:',e)
    return jsonify(resp)

@app.route('/audit/', methods=['GET'])
@auth.login_required
def auditView():
    resp = {'status':False}
    sql = ' SELECT * FROM AUDIT_TRAIL LIMIT 150; '
    mapRowsSelected = {
        'TIMESTAMP':0,
        'PN':1,
        'NAME':2,
        'TYPE':3,
        'MESSAGE':4
        }
    if sql != '':
        data = []
        #Prod
        rows = db.selectData(sql,dbMDO)

        #Dev
        #rows = db.selectData(sql,dbDEV)
        for row in rows:
            try:
                data.append({
                    'TIMESTAMP':row[mapRowsSelected['TIMESTAMP']],
                    'PN':row[mapRowsSelected['PN']],
                    'NAME':row[mapRowsSelected['NAME']],
                    'TYPE':row[mapRowsSelected['TYPE']],
                    'MESSAGE':row[mapRowsSelected['MESSAGE']],
                    })
            except Exception as e:
                myLogger.logging_error('flask', 'error looping response audit view, e:', e)
        resp['data'] = data
        resp['status'] = True
    else : 
        resp['message'] = 'fail to generate query for audit view'
    return jsonify(resp)

@app.route('/hourly-report/view', methods=['GET'])
@auth.login_required
def hourlyReportView():
    return "hourly report View coming soon"

@app.route('/hourly-report/insert', methods=['POST'])
@auth.login_required
def hourlyReportInsert():
    return "hourly report Insert coming soon"


@app.route("/hello", methods=['GET'])
def hellow():
   
    if 1+1 == 2:
        return "Working From 172.18.141.41"
    else : 
        return "Not Working"
    
@app.route("/get-fds")
@auth.login_required
def getFraudCheckService():
    resp = {'status':False}
    sql = " SELECT * FROM BRI_SERVICE_DUMMY WHERE DO_FRAUD_CHECK IN ('Y','N') LIMIT 150; "
    mapRowsSelected = {
        'SERVICE_ID':0,
        'AGGREGATOR_ID':1,
        'TRX_TYPE_ID':2,
        'LIMIT_TYPE_ID':3,
        'ESB_SVC_NAME':4,
        'ADVANCE_SVC_NAME':5,
        'SERVICE_DESC':6,
        'IS_CONDITIONAL_FEE':7,
        'EXISTING_REMARK_FORMULA':8,
        'EXISTING_REMARK2_FORMULA':9,
        'DO_FRAUD_CHECK':10
        }
    if sql != '':
        data = []
        #prod
        rows = db.selectData(sql,dbMDO)
        
        #dev
        #rows = db.selectData(sql,dbDEV)
        # return str(len(rows))
        for row in rows:
            try:
                data.append({
                    'SERVICE_ID':row[mapRowsSelected['SERVICE_ID']],
                    'AGGREGATOR_ID':row[mapRowsSelected['AGGREGATOR_ID']],
                    'TRX_TYPE_ID':row[mapRowsSelected['TRX_TYPE_ID']],
                    'LIMIT_TYPE_ID':row[mapRowsSelected['LIMIT_TYPE_ID']],
                    'ESB_SVC_NAME':row[mapRowsSelected['ESB_SVC_NAME']],
                    'ADVANCE_SVC_NAME':row[mapRowsSelected['ADVANCE_SVC_NAME']],
                    'SERVICE_DESC':row[mapRowsSelected['SERVICE_DESC']],
                    'IS_CONDITIONAL_FEE':row[mapRowsSelected['IS_CONDITIONAL_FEE']],
                    'EXISTING_REMARK_FORMULA':row[mapRowsSelected['EXISTING_REMARK_FORMULA']],
                    'EXISTING_REMARK2_FORMULA':row[mapRowsSelected['EXISTING_REMARK2_FORMULA']],
                    'DO_FRAUD_CHECK':row[mapRowsSelected['DO_FRAUD_CHECK']]
                    })
            except Exception as e:
                myLogger.logging_error('flask', 'error getFraudCheckService, e:', e)
        resp['data'] = data
        resp['status'] = True
        resp['count'] = len(rows)
    else : 
        resp['message'] = 'fail to generate query'
    return jsonify(resp)

def updateFraudCheckService(service_id, value):
    sqlUpdate = f""" UPDATE BRI_SERVICE_DUMMY SET
        DO_FRAUD_CHECK = '{value}'
        WHERE SERVICE_ID IN ({service_id});
        """
    #prod
    result = db.executeQuery(sqlUpdate, dbMDO)

    #dev
    #result = db.executeQuery(sqlUpdate, dbDEV)
    return result

@app.route("/disable-fds", methods=['POST'])
@auth.login_required
def disableFraudCheckService():
    resp = {'status':False}
    data = request.get_json()
    service = data["SERVICE_ID"]
    serviceString = ', '.join(map("'{0}'".format, service))
    if len(serviceString) == 0 : 
        return f'Empty Service IDs'

    sqlSelect = f" SELECT * FROM BRI_SERVICE_DUMMY WHERE SERVICE_ID IN ({serviceString}) LIMIT 150; "
    mapRowsSelected = {
        'SERVICE_ID':0,
        'AGGREGATOR_ID':1,
        'TRX_TYPE_ID':2,
        'LIMIT_TYPE_ID':3,
        'ESB_SVC_NAME':4,
        'ADVANCE_SVC_NAME':5,
        'SERVICE_DESC':6,
        'IS_CONDITIONAL_FEE':7,
        'EXISTING_REMARK_FORMULA':8,
        'EXISTING_REMARK2_FORMULA':9,
        'DO_FRAUD_CHECK':10
        }
    
    if len(sqlSelect) != 0:
        data = []
        result = updateFraudCheckService(serviceString, 'N')
        
        #prod
        rows = db.selectData(sqlSelect,dbMDO)

        #dev
        #rows = db.selectData(sqlSelect,dbDEV)

        for row in rows:
            try:
                data.append({
                    'SERVICE_ID':row[mapRowsSelected['SERVICE_ID']],
                    'AGGREGATOR_ID':row[mapRowsSelected['AGGREGATOR_ID']],
                    'TRX_TYPE_ID':row[mapRowsSelected['TRX_TYPE_ID']],
                    'LIMIT_TYPE_ID':row[mapRowsSelected['LIMIT_TYPE_ID']],
                    'ESB_SVC_NAME':row[mapRowsSelected['ESB_SVC_NAME']],
                    'ADVANCE_SVC_NAME':row[mapRowsSelected['ADVANCE_SVC_NAME']],
                    'SERVICE_DESC':row[mapRowsSelected['SERVICE_DESC']],
                    'IS_CONDITIONAL_FEE':row[mapRowsSelected['IS_CONDITIONAL_FEE']],
                    'EXISTING_REMARK_FORMULA':row[mapRowsSelected['EXISTING_REMARK_FORMULA']],
                    'EXISTING_REMARK2_FORMULA':row[mapRowsSelected['EXISTING_REMARK2_FORMULA']],
                    'DO_FRAUD_CHECK':row[mapRowsSelected['DO_FRAUD_CHECK']]
                    })
            except Exception as e:
                myLogger.logging_error('flask', 'error disableFraudCheckService, e:', e)
        resp['data'] = data
        resp['status'] = True
        resp['count'] = len(rows)
        resp['result'] = result

    # return f'Query : {sql}'
    return jsonify(resp)

    # resp = {'status':False}
    
@app.route("/enable-fds", methods=['POST'])
@auth.login_required
def enableFraudCheckService():
    resp = {'status':False}
    data = request.get_json()
    service = data["SERVICE_ID"]
    serviceString = ', '.join(map("'{0}'".format, service))
    if len(serviceString) == 0 : 
        return f'Empty Service IDs'

    sqlSelect = f" SELECT * FROM BRI_SERVICE_DUMMY WHERE SERVICE_ID IN ({serviceString}) LIMIT 150; "
    mapRowsSelected = {
        'SERVICE_ID':0,
        'AGGREGATOR_ID':1,
        'TRX_TYPE_ID':2,
        'LIMIT_TYPE_ID':3,
        'ESB_SVC_NAME':4,
        'ADVANCE_SVC_NAME':5,
        'SERVICE_DESC':6,
        'IS_CONDITIONAL_FEE':7,
        'EXISTING_REMARK_FORMULA':8,
        'EXISTING_REMARK2_FORMULA':9,
        'DO_FRAUD_CHECK':10
        }
    
    if len(sqlSelect) != 0:
        data = []
        result = updateFraudCheckService(serviceString, 'Y')
        
        #prod
        rows = db.selectData(sqlSelect,dbMDO)
        
        #dev
        #rows = db.selectData(sqlSelect,dbDEV)
        for row in rows:
            try:
                data.append({
                    'SERVICE_ID':row[mapRowsSelected['SERVICE_ID']],
                    'AGGREGATOR_ID':row[mapRowsSelected['AGGREGATOR_ID']],
                    'TRX_TYPE_ID':row[mapRowsSelected['TRX_TYPE_ID']],
                    'LIMIT_TYPE_ID':row[mapRowsSelected['LIMIT_TYPE_ID']],
                    'ESB_SVC_NAME':row[mapRowsSelected['ESB_SVC_NAME']],
                    'ADVANCE_SVC_NAME':row[mapRowsSelected['ADVANCE_SVC_NAME']],
                    'SERVICE_DESC':row[mapRowsSelected['SERVICE_DESC']],
                    'IS_CONDITIONAL_FEE':row[mapRowsSelected['IS_CONDITIONAL_FEE']],
                    'EXISTING_REMARK_FORMULA':row[mapRowsSelected['EXISTING_REMARK_FORMULA']],
                    'EXISTING_REMARK2_FORMULA':row[mapRowsSelected['EXISTING_REMARK2_FORMULA']],
                    'DO_FRAUD_CHECK':row[mapRowsSelected['DO_FRAUD_CHECK']]
                    })
            except Exception as e:
                myLogger.logging_error('flask', 'error enableFraudCheckService, e:', e)
        resp['data'] = data
        resp['status'] = True
        resp['count'] = len(rows)
        resp['result'] = result

    # return f'Query : {sql}'
    return jsonify(resp)


@app.route("/launch-ansible", methods=['POST'])
def launch_job():
    try:
        responseAnsible = requests.post(f"http://{AWX_IP}/api/v2/job_templates/{JOB_TEMPLATE_ID}/launch/", headers=HEADERS)
        responseAnsible.raise_for_status()
        return "Pekerjaan berhasil diluncurkan."
    except requests.exceptions.RequestException as e:
        return "Pekerjaan berhasil diluncurkan."
        # print("Gagal meluncurkan pekerjaan:", e)
        # print(responseAnsible.text)


## KONFIGURASI LOGON REMOVE AUTOMATION

@app.route("/ssh-remove-au", methods=['POST'])
def launch_removeau():
    try:
        # Inisialisasi koneksi SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port, username, password)

        # Upload file 1
        sftp = ssh.open_sftp()
        sftp.put(os.path.join(local_dir1, local_file1), os.path.join(remote_dir1, local_file1))
        sftp.close()

        # Upload file 2
        sftp = ssh.open_sftp()
        sftp.put(os.path.join(local_dir2, local_file2), os.path.join(remote_dir2, local_file2))
        sftp.close()

        # Jalankan perintah chmod dan file conndown2.sh
        stdin, stdout, stderr = ssh.exec_command(f'chmod 775 {remote_dir2}/{local_file2}')
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        if error:
            print(f"Error running chmod command: {error}")
        else:
            print("chmod command executed successfully.")

        # Jalankan perintah conndown2.sh dengan parameter AUTOMATION
        stdin1, stdout1, stderr1 = ssh.exec_command(f'{remote_dir2}/{local_file2} 7168', get_pty=True)
        error1 = stderr1.read().decode().strip()

        stdin2, stdout2, stderr2 = ssh.exec_command(f'{remote_dir2}/{local_file2} 7169', get_pty=True)
        error2 = stderr2.read().decode().strip()
        if error:
            return (f"Error running conndown2.sh command: {error}")
        else:
            return "Pekerjaan berhasil diluncurkan."
        
    finally:
        # Tutup koneksi SSH
        ssh.close()

@app.route("/ssh-logon-au", methods=['POST'])
def launch_logonau():
    try:
        # Inisialisasi koneksi SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port, username, password)

        # Upload file 1
        sftp = ssh.open_sftp()
        sftp.put(os.path.join(local_dir3, local_file3), os.path.join(remote_dir3, local_file3))
        sftp.close()

        # Upload file 2
        sftp = ssh.open_sftp()
        sftp.put(os.path.join(local_dir4, local_file4), os.path.join(remote_dir4, local_file4))
        sftp.close()

        # Jalankan perintah chmod dan file conndown2.sh
        stdin, stdout, stderr = ssh.exec_command(f'chmod 775 {remote_dir4}/{local_file4}')
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        if error:
            print(f"Error running chmod command: {error}")
        else:
            print("chmod command executed successfully.")

        # Jalankan perintah conndown2.sh dengan parameter AUTOMATION
        stdin1, stdout1, stderr1 = ssh.exec_command(f'{remote_dir4}/{local_file4} 7168', get_pty=True)
        error1 = stderr1.read().decode().strip()

        stdin2, stdout2, stderr2 = ssh.exec_command(f'{remote_dir4}/{local_file4} 7169', get_pty=True)
        error2 = stderr2.read().decode().strip()

        if error:
            return (f"Error running conndown2.sh command: {error}")
        else:
            return "Pekerjaan berhasil diluncurkan."
        
    finally:
        # Tutup koneksi SSH
        ssh.close()


## KONFIGURASI LOGON REMOVE 7168

@app.route("/ssh-remove-7168", methods=['POST'])
def launch_remove7168():
    try:
        # Inisialisasi koneksi SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port, username, password)

        # Upload file 1
        sftp = ssh.open_sftp()
        sftp.put(os.path.join(local_dir1, local_file1), os.path.join(remote_dir1, local_file1))
        sftp.close()

        # Upload file 2
        sftp = ssh.open_sftp()
        sftp.put(os.path.join(local_dir2, local_file2), os.path.join(remote_dir2, local_file2))
        sftp.close()

        # Jalankan perintah chmod dan file conndown2.sh
        stdin, stdout, stderr = ssh.exec_command(f'chmod 775 {remote_dir2}/{local_file2}')
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        if error:
            print(f"Error running chmod command: {error}")
        else:
            print("chmod command executed successfully.")

        # Jalankan perintah conndown2.sh dengan parameter 7168
        stdin1, stdout1, stderr1 = ssh.exec_command(f'{remote_dir2}/{local_file2} 7168', get_pty=True)
        error1 = stderr1.read().decode().strip()

        if error:
            return (f"Error running conndown2.sh command: {error}")
        else:
            return "Pekerjaan berhasil diluncurkan."
        
    finally:
        # Tutup koneksi SSH
        ssh.close()
        
@app.route("/ssh-logon-7168", methods=['POST'])
def launch_logon7168():
    try:
        # Inisialisasi koneksi SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port, username, password)

        # Upload file 1
        sftp = ssh.open_sftp()
        sftp.put(os.path.join(local_dir3, local_file3), os.path.join(remote_dir3, local_file3))
        sftp.close()

        # Upload file 2
        sftp = ssh.open_sftp()
        sftp.put(os.path.join(local_dir4, local_file4), os.path.join(remote_dir4, local_file4))
        sftp.close()

        # Jalankan perintah chmod dan file conndown2.sh
        stdin, stdout, stderr = ssh.exec_command(f'chmod 775 {remote_dir4}/{local_file4}')
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        if error:
            print(f"Error running chmod command: {error}")
        else:
            print("chmod command executed successfully.")

        # Jalankan perintah conndown2.sh dengan parameter 7168
        stdin1, stdout1, stderr1 = ssh.exec_command(f'{remote_dir4}/{local_file4} 7168', get_pty=True)
        error1 = stderr1.read().decode().strip()

        if error:
            return (f"Error running conndown2.sh command: {error}")
        else:
            return "Pekerjaan berhasil diluncurkan."
        
    finally:
        # Tutup koneksi SSH
        ssh.close()

## KONFIGURASI LOGON REMOVE 7169

@app.route("/ssh-remove-7169", methods=['POST'])
def launch_remove7169():
    try:
        # Inisialisasi koneksi SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port, username, password)

        # Upload file 1
        sftp = ssh.open_sftp()
        sftp.put(os.path.join(local_dir1, local_file1), os.path.join(remote_dir1, local_file1))
        sftp.close()

        # Upload file 2
        sftp = ssh.open_sftp()
        sftp.put(os.path.join(local_dir2, local_file2), os.path.join(remote_dir2, local_file2))
        sftp.close()

        # Jalankan perintah chmod dan file conndown2.sh
        stdin, stdout, stderr = ssh.exec_command(f'chmod 775 {remote_dir2}/{local_file2}')
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        if error:
            print(f"Error running chmod command: {error}")
        else:
            print("chmod command executed successfully.")

        # Jalankan perintah conndown2.sh dengan parameter 7168
        stdin1, stdout1, stderr1 = ssh.exec_command(f'{remote_dir2}/{local_file2} 7169', get_pty=True)
        error1 = stderr1.read().decode().strip()

        if error:
            return (f"Error running conndown2.sh command: {error}")
        else:
            return "Pekerjaan berhasil diluncurkan."
        
    finally:
        # Tutup koneksi SSH
        ssh.close()
        
@app.route("/ssh-logon-7169", methods=['POST'])
def launch_logon7169():
    try:
        # Inisialisasi koneksi SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port, username, password)

        # Upload file 1
        sftp = ssh.open_sftp()
        sftp.put(os.path.join(local_dir3, local_file3), os.path.join(remote_dir3, local_file3))
        sftp.close()

        # Upload file 2
        sftp = ssh.open_sftp()
        sftp.put(os.path.join(local_dir4, local_file4), os.path.join(remote_dir4, local_file4))
        sftp.close()

        # Jalankan perintah chmod dan file conndown2.sh
        stdin, stdout, stderr = ssh.exec_command(f'chmod 775 {remote_dir4}/{local_file4}')
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        if error:
            print(f"Error running chmod command: {error}")
        else:
            print("chmod command executed successfully.")

        # Jalankan perintah conndown2.sh dengan parameter 7169
        stdin1, stdout1, stderr1 = ssh.exec_command(f'{remote_dir4}/{local_file4} 7169', get_pty=True)
        error1 = stderr1.read().decode().strip()

        if error:
            return (f"Error running conndown2.sh command: {error}")
        else:
            return "Pekerjaan berhasil diluncurkan."
        
    finally:
        # Tutup koneksi SSH
        ssh.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3131)
    
