from flask import Flask,request,jsonify
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
import myLogger
import requests
import pandas as pd
import databaseMySql as db

USER_DATA = {
    "admin": "SuperSecretPwd"
}

app = Flask(__name__)
CORS(app)

auth = HTTPBasicAuth()

dbMDO = {
    'host' : "172.18.141.41",
    'database' : 'MDO',
    'username' : 'administrator',
    'password' : 'P@ssw0rd123'
}


@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password

@app.route('/grafanaNotify/', methods=['POST'])
# @auth.login_required
def grafanaNotify():
    resp = {'status':False}
    body = request.json
    myLogger.logging_info('flask','/grafanaNotify/ \t','body:',body,'\t')

    response = jsonify(resp)
    return response

@app.route('/login/', methods=['POST'])
@auth.login_required
def login():
    resp = {'status':False}
    body = request.json
    try:
        url = 'https://apiclose.bri.co.id/gateway/apiActiveDirectory/1.0/ADAuthentication2'
        headers = {"Authorization":"Basic Y29udGFjdENlbnRlcjpDMG50NGN0QzNudGVyITE0MDE3","Content-Type":"application/json"}
        myLogger.logging_info('flask','/login/ \t','body:',body,'\t')
        # json = body
        response = requests.post(url,headers=headers,json = body)
        jsonResp = response.json()
        myLogger.logging_info('flask','/ADAuthentication2/ \t','jsonResp:',jsonResp,'\t')
        if jsonResp['responseCode'] == '00':
            #inquiry pn detail
            resp['status'] = True
            url = 'https://apiclose.bri.co.id/gateway/apiBristars/1.0/pekerja/inquiryPekerjaByPn'
            headers = {"Authorization":"Basic Y29udGFjdENlbnRlcjpDMG50NGN0QzNudGVyITE0MDE3","Content-Type":"application/json"}
            response_detail_pn = requests.post(url,headers=headers,json = {'pernr':body['userLogin']})
            json_response_detail_pn = response_detail_pn.json()
            myLogger.logging_info('flask','/inquiryPekerjaByPn/ \t','jsonResp:',json_response_detail_pn,'\t')
            resp['data'] = json_response_detail_pn['responseData']
            resp['data']['email'] = jsonResp['responseMessage']
        else :
            resp['message'] = 'Invalid Credentials'
        myLogger.logging_info('flask','/login/ \t','response:',response.json(),'\t')
    except Exception as e:
        myLogger.logging_error('flask','got error login,e:',e)
    return jsonify(resp)

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
@auth.login_required
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
        rows = db.selectData(sql,dbMDO)
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
        result = db.executeQuery(sql, dbMDO)
        insertHistoryStatus = db.executeQuery(sqlInsertHist, dbMDO)
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
    sqlSelectHist = 'SELECT * FROM BRI_SERVICE_HISTORY WHERE UPDATED_SERVICE_ID = \'' + serviceId + '\';'
    mapRowsSelected = {
        'OLD_SERVICE_ID':0,
        'UPDATED_SERVICE_ID':1,
        'STATUS':2
    }
    try:
        data = []
        rows = db.selectData(sqlSelectHist,dbMDO)
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
            result = db.executeQuery(sql,dbMDO)
            deleteStatus = db.executeQuery(sqlDeleteHist, dbMDO)
            resp['result'] = result
            resp['deleteStatus'] = deleteStatus
            resp['status'] = True
        except Exception as e:
            myLogger.logging_error('flask', 'enable service failed (esbEnable), e:',e)    

    except Exception as e:
        myLogger.logging_error('flask', 'enable service failed (esbEnable), e:',e)

    return jsonify(resp)

        
@app.route("/hello")
def hellow():
    if 1+1 == 2:
        return "Working From 172.18.141.41"
    else : 
        return "Not Working"
    
    
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3131)