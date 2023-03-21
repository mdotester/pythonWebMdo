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

def selectQueryUpdateCacheESB(bodyReq):
    sql = ' SELECT * FROM ListIPESB '
    arrWhereNodeType = []
    arrWhereSiteType = []
    

    if bodyReq['isGW']:
        arrWhereNodeType.append(" ESBType = 'GW' ")
    if bodyReq['isISOGW']:
        arrWhereNodeType.append(" ESBType = 'ISOGW' ")
    if bodyReq['isBLMON']:
        arrWhereNodeType.append(" ESBType = 'BLMON' ")
    if bodyReq['isBLNONMON']:
        arrWhereNodeType.append(" ESBType = 'BLNONMON' ")
    if bodyReq['isPLCORE']:
        arrWhereNodeType.append(" ESBType = 'PLCORE' ")
    if bodyReq['isPLCARD']:
        arrWhereNodeType.append(" ESBType = 'PLCARD' ")
    if bodyReq['isDC']:
        arrWhereSiteType.append(" Site = 'DC' ")
    if bodyReq['isDRC']:
        arrWhereSiteType.append(" Site = 'DRC' ")
    if bodyReq['isODC']:
        arrWhereSiteType.append(" Site = 'ODC' ")
    
    sqlWhereNodeType = ' OR '.join(arrWhereNodeType)
    sqlWhereSiteType = ' OR '.join(arrWhereSiteType)

    sql = sql + ' WHERE (' + sqlWhereNodeType + ') AND (' + sqlWhereSiteType + ');'
    return sql


    
    
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3131)