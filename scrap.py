import requests
from bs4 import BeautifulSoup
import  mysql.connector as sql
db = sql.connect(
    host="localhost",
    user="root",
    password="",
    database="python_test"
)
cursor = db.cursor()

res = requests.get("http://127.0.0.1:5500/scrapeThis.html")
resText = res.text
 
bSoup = BeautifulSoup(resText,'html.parser')
table = bSoup.find('table')
# headers = [x.text for x in table.find_all("th")]
tableRows = table.find_all("tr")
rows = []
for row in tableRows:
    rows.append([x.text for x in row.find_all('td')])

newList = [tuple(([""]+x[1:7])) for x in rows]
newList = newList[1:]

print(newList[0])
for val in newList:
    cursor.execute("insert into tasks values(%s,%s,%s,%s,%s,%s,%s,NULL)",val)
    db.commit()
    print(cursor.rowcount)
    
# tableData = []
# for row in rows:
#     if len(row)==len(headers):
#         obj = {val:row[idx] for idx, val in enumerate(headers)}
#         tableData.append(obj)

# for i in range(0,len(tableData)):
    # print(tableData[i]['Created By'])
    # tableData[i] = 'NULL'
    # print(tuple(x.values()))
# for x in tableData:
    # print(x)
# for row in tableData:
#     values = tuple([val for val in row.values()])
#     cursor.execute("insert into test values(%s,%s,%s,%s,%s,%s)",values)
#     db.commit()
#     print(cursor.rowcount)

