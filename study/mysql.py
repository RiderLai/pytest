import pymysql

conn = pymysql.connect("10.1.136.10", "python", "python", "testDB")
cursor = conn.cursor()
cursor.execute("Select  * From user limit 100")
data = cursor.fetchmany()
print(data)
conn.close()