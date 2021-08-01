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

HOUSEHOLD = '''SELECT distinct(dbo.[400_households].HSHD_NUM), COUNT(dbo.[400_products].COMMODITY) AS Total_Alc_Sales
FROM ((dbo.[400_households]
	RIGHT JOIN dbo.[400_transactions] ON dbo.[400_transactions].HSHD_NUM = dbo.[400_households].HSHD_NUM)
	RIGHT JOIN dbo.[400_products] on dbo.[400_products].PRODUCT_NUM = dbo.[400_transactions].PRODUCT_NUM)
WHERE dbo.[400_products].COMMODITY = 'ALCOHOL' AND dbo.[400_transactions].YEAR IN ({}) AND dbo.[400_households].HSHD_NUM = {}
GROUP BY dbo.[400_households].HSHD_NUM'''

HSHDNUMYEARALCSALESCOUNT = '''SELECT COUNT(dbo.[400_products].COMMODITY) AS Total_Alc_Sales
FROM ((dbo.[400_households]
	RIGHT JOIN dbo.[400_transactions] ON dbo.[400_transactions].HSHD_NUM = dbo.[400_households].HSHD_NUM)
	RIGHT JOIN dbo.[400_products] on dbo.[400_products].PRODUCT_NUM = dbo.[400_transactions].PRODUCT_NUM)
WHERE dbo.[400_products].COMMODITY = 'ALCOHOL' AND dbo.[400_transactions].YEAR IN (?) AND dbo.[400_households].HSHD_NUM = ?
GROUP BY dbo.[400_households].HSHD_NUM
'''

HSHDNUMYEARALCSALESCOST = '''SELECT SUM(CAST(dbo.[400_transactions].SPEND AS float)) AS Total_Alc_Sales_Cost
FROM ((dbo.[400_households]
	RIGHT JOIN dbo.[400_transactions] ON dbo.[400_transactions].HSHD_NUM = dbo.[400_households].HSHD_NUM)
	RIGHT JOIN dbo.[400_products] on dbo.[400_products].PRODUCT_NUM = dbo.[400_transactions].PRODUCT_NUM)
WHERE dbo.[400_products].COMMODITY = 'ALCOHOL' AND dbo.[400_transactions].YEAR IN (?) AND dbo.[400_households].HSHD_NUM = ?
GROUP BY dbo.[400_households].HSHD_NUM
'''

HSHDNUMCHILDRENALCSALECOST = '''SELECT distinct(dbo.[400_households].CHILDREN) as Num_Children, SUM(CAST(dbo.[400_transactions].SPEND AS float)) AS Total_Alc_Sales_Cost
FROM ((dbo.[400_households]
	RIGHT JOIN dbo.[400_transactions] ON dbo.[400_transactions].HSHD_NUM = dbo.[400_households].HSHD_NUM)
	RIGHT JOIN dbo.[400_products] on dbo.[400_products].PRODUCT_NUM = dbo.[400_transactions].PRODUCT_NUM)
WHERE dbo.[400_products].COMMODITY = 'ALCOHOL' AND dbo.[400_households].CHILDREN != 'null' AND dbo.[400_transactions].YEAR IN (?)
GROUP BY dbo.[400_households].CHILDREN;
'''

HSHDINCOMERANGEALCSALECOST = '''SELECT distinct(dbo.[400_households].INCOME_RANGE) as Income_Range, SUM(CAST(dbo.[400_transactions].SPEND AS float)) AS Total_Alc_Sales_Cost
FROM ((dbo.[400_households]
	RIGHT JOIN dbo.[400_transactions] ON dbo.[400_transactions].HSHD_NUM = dbo.[400_households].HSHD_NUM)
	RIGHT JOIN dbo.[400_products] on dbo.[400_products].PRODUCT_NUM = dbo.[400_transactions].PRODUCT_NUM)
WHERE dbo.[400_products].COMMODITY = 'ALCOHOL' AND dbo.[400_households].CHILDREN != 'null' AND dbo.[400_transactions].YEAR IN (?)
GROUP BY dbo.[400_households].INCOME_RANGE
ORDER BY Total_Alc_Sales_Cost DESC;
'''

HSHDDATA = '''dbo.[400_transactions].BASKET_NUM, dbo.[400_transactions].PRODUCT_NUM, dbo.[400_products].COMMODITY, dbo.[400_products].DEPARTMENT
from dbo.[400_transactions]
Inner Join dbo.[400_products] ON dbo.[400_transactions].PRODUCT_NUM = dbo.[400_products].PRODUCT_NUM
where dbo.[400_transactions].HSHD_NUM = (?) AND dbo.[400_transactions].YEAR IN (?);
'''

class DB():
	def getHouseHoldData(self, hshd_num, year):
		vals = self.cur.execute(HSHDDATA, [hshd_num, year])
		if vals is not None:
			rows = []
			for idx in vals:
				rows.append(idx)
			return rows
		else:
			return None
			
	def getHouseHoldAlcSalesCount(self, hshd_num, year):
		self.cur.execute(HSHDNUMYEARALCSALESCOUNT, [year, hshd_num])
		row = self.cur.fetchone()
		if row is not None:
			return row.Total_Alc_Sales
		else:
			return None
	
	def getHouseHoldChildrenAlcSaleCost(self, year):
		# This method returns 3 rows with 2 columns. Column 1 represents the number of children in a household (1, 2, 3+)
		# Column 2 represents the sum of the cost of alcohol sales for households with some number of children.
		# The year is passed as a parameter.
		val = self.cur.execute(HSHDNUMCHILDRENALCSALECOST, [year])
		rows = []
		for idx in val:
			rows.append(idx)
		return rows
	
	def getHouseHoldIncomeRangeAlcSaleCost(self, year):
		# This method returns 6 rows with 2 columns. Column 1 represents the income range.
		# Column 2 represents the sum of the cost of alcohol sales for households with certain income ranges.
		# The year is passed as a parameter.
		val = self.cur.execute(HSHDINCOMERANGEALCSALECOST, [year])
		rows = []
		for idx in val:
			rows.append(idx)
		return rows

	def getHouseHoldAlcSalesCost(self, hshd_num, year):
		self.cur.execute(HSHDNUMYEARALCSALESCOST, [year, hshd_num])
		row = self.cur.fetchone()
		if row is not None:
			return row.Total_Alc_Sales_Cost
		else:
			return None

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
			
			
			