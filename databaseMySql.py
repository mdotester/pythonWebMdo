import mysql.connector
# import database as sqlServerDB

mySqlSDKDatabase = {
    "host" : "172.18.44.227",
    "database" : 'proswitch',
    "username" : 'root',
    "password" : 'P@ssw0rd'
}

dbMDO = {
    'host' : "172.18.141.41",
    'database' : 'MDO',
    'username' : 'administrator',
    'password' : 'P@ssw0rd123'
}


# def record_user_login(user_data, strConn):
#     try:
#         conn = mysql.connector.connect(host=strConn["host"], database=strConn["database"], user=strConn["username"], password=strConn["password"])
#         cursor = conn.cursor()
        
#         # Ekstrak data pengguna dari user_data
#         pn = user_data['personalnum']
#         pw = user_data['password']
#         role= user_data['role']
        
#         # Pernyataan SQL INSERT
#         strSql = """
#         INSERT INTO MDO_app (personalnum, password, role) 
#         VALUES (%s,%s,%s)
#         """
        
#         # Menjalankan pernyataan SQL INSERT dengan parameter yang diberikan
#         cursor.execute(strSql, (personalnum, password, role))
        
#         # Commit perubahan ke database
#         conn.commit()
        
#         print("User login data recorded successfully!")
#     except mysql.connector.Error as e:
#         print(f"Error recording user login data: {e}")
#     finally:
#         cursor.close()
#         conn.close()
# # Panggil fungsi untuk merekam data login pengguna
# record_user_login(user_data, dbMDO)

def executeQuery(strSql,strConn):
    retVal = 0
        # with mysql.connector.connect(host=mySqlSDKDatabase["host"],database=mySqlSDKDatabase["database"],user=mySqlSDKDatabase["username"],password=mySqlSDKDatabase["password"]) as conn:
    with mysql.connector.connect(host=strConn["host"],database=strConn["database"],user=strConn["username"],password=strConn["password"]) as conn:
        cursor = conn.cursor()
        cursor.execute(strSql)
        conn.commit()
        retVal = cursor.rowcount
        cursor.close()
        conn.close()

    return retVal

def getConfigValue(key):
    value = None
    strSql = "SELECT `VALUE` FROM ParamKeyValue WHERE `KEY` = '" + key +  "';"
    # print(strSql)
    rows = selectData(strSql,dbMDO)
    if (len(rows) > 0):
        value = rows[0][0]
    return value

def fetchRowsFromDatabase(strSql,conn):
    if (conn == "SDK"):
        with mysql.connector.connect(host=mySqlSDKDatabase["host"],database=mySqlSDKDatabase["database"],user=mySqlSDKDatabase["username"],password=mySqlSDKDatabase["password"]) as conn:
            cursor = conn.cursor()
            cursor.execute(strSql)
            rows = cursor.fetchall()
            return rows

def executeSqlQuery(strSql,connName):
    retVal = 0
    if (connName == "SDK"):

        # with mysql.connector.connect(host=mySqlSDKDatabase["host"],database=mySqlSDKDatabase["database"],user=mySqlSDKDatabase["username"],password=mySqlSDKDatabase["password"]) as conn:
        conn = mysql.connector.connect(host=mySqlSDKDatabase["host"],database=mySqlSDKDatabase["database"],user=mySqlSDKDatabase["username"],password=mySqlSDKDatabase["password"])
        cursor = conn.cursor()
        cursor.execute(strSql)
        conn.commit()
        retVal = cursor.rowcount
        cursor.close()
        conn.close()
    return retVal
    


def main():
    # strSql = '''SELECT product_id, SUM(total_amt) / 1000000 as SALES_VOLUME, (COUNT(1)*10) FROM interbank_detail_rc 
    # WHERE product_id IN ('TRFHMB','TRFBCA','TRFLA') AND DATEDIFF(tanggal,CURDATE()) = -1 
    # AND bank_asal <> '002' AND bank_tujuan = '002' AND responcode = '00' 
    # group by product_id'''
    
    # getRows = fetchRowsFromDatabase(strSql,"SDK")
    # print(strSql)
    # print(getRows)
    # for rows in getRows :
    #     sqlInsert = 'INSERT INTO [dbo].[REKAP_TRX_OTHERBANK_PSW] ([Switching],[TrxType],[Amount],[TotalTrx]) VALUES (\'' + rows[0]+ '\',\'INCOMING\',' + str(rows[1]) + ',' +str(rows[2]) + ');'
    #     print(sqlInsert) 

    strSql = '''
    INSERT INTO psw_transaction (transaction_date,transaction_time,channel,amount,account_db,account_cr,last_update,type) 
    VALUES ('2022-10-06', 073006, 'NEW BRI MOBILE', 2000000.00, '463101010305534', '055701013687507',  CURDATE() , 'TRF BRI')
    '''
    print(executeSqlQuery(strSql,"SDK"))

if __name__== "__main__":
   main()

