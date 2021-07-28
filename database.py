import pyodbc
server = 'cs6165-cc-final-project.database.windows.net'
database = '8451_The_Complete_Journey_2_Sample'
username = 'azureuser'
password = '{CloudComp1234$#@!}'   
driver= '{ODBC Driver 17 for SQL Server}'

ALCSALES = '''select trim(pro.COMMODITY), tra.Year, SUM(CAST(tra.SPEND as float)) as Spend from dbo.[400_transactions] AS tra
Inner Join dbo.[400_products] as pro
ON tra.PRODUCT_NUM = pro.PRODUCT_NUM
where trim(pro.COMMODITY) = 'ALCOHOL' and tra.Year in (2019,2020)
GROUP BY pro.COMMODITY, tra.Year'''

AUTOSALES = '''select pro.COMMODITY, tra.Year, SUM(CAST(tra.SPEND as float)) as Spend from dbo.[400_transactions] AS tra
Inner Join dbo.[400_products] as pro
ON tra.PRODUCT_NUM = pro.PRODUCT_NUM
where pro.COMMODITY = 'AUTO' and tra.Year in (2019,2020)
GROUP BY pro.COMMODITY, tra.Year;'''

TOTALSALES = '''select tra.Year, SUM(CAST(tra.SPEND as float)) as Spend from dbo.[400_transactions] AS tra
Inner Join dbo.[400_products] as pro
ON tra.PRODUCT_NUM = pro.PRODUCT_NUM
where Year in (2019,2020)
Group By tra.Year;'''

HOUSEHOLD = ''' '''

class DB():
	def getDataHouseHold(self, houseHld):
		return

	def getAlcSales(self):
		val = self.cur.execute(ALCSALES)
		rows = []
		for idx in val:
			rows.append(idx)
		return rows
	
	def getAutoSales(self):
		val = self.cur.execute(AUTOSALES)
		rows = []
		for idx in val:
			rows.append(idx)
		return rows

	def getTotalSales(self):
		val = self.cur.execute(TOTALSALES)
		rows = []
		for idx in val:
			rows.append(idx)
		return rows

	def __init__(self):
		self.cur = object
		with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
			self.cur = conn.cursor()
			
			
			