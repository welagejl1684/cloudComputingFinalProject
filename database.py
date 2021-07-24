import pyodbc
server = 'cs6165-cc-final-project.database.windows.net'
database = '8451_The_Complete_Journey_2_Sample'
username = 'azureuser'
password = '{CloudComp1234$#@!}'   
driver= '{ODBC Driver 17 for SQL Server}'

QUERY = "SELECT dbo.[400_households].HSHD_NUM, dbo.[400_transactions].BASKET_NUM FROM dbo.[400_households], dbo.[400_transactions] WHERE dbo.[400_households].HSHD_NUM = dbo.[400_transactions].HSHD_NUM"

with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute(QUERY)
        row = cursor.fetchone()
        while row:
            print (str(row[0]) + " " + str(row[1]))
            row = cursor.fetchone()