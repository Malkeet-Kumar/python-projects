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

res = requests.get("https://fnec.cornell.edu/for-participants/recipe-table/")
resText = res.text
 
bSoup = BeautifulSoup(resText,'html.parser')
table = bSoup.find('table',id="tablepress-67")
headers = [x.text for x in table.find_all("th")]
tableRows = table.find_all("tr")
rows = []
for row in tableRows:
    tRow = []
    for td in row.find_all("td"):
        tRow.append(td.text)
    rows.append(tRow)

tableData = []
for row in rows:
    if len(row)==len(headers):
        obj = {val:row[idx] for idx, val in enumerate(headers)}
        tableData.append(obj)

for row in tableData:
    values = tuple([val for val in row.values()])
    cursor.execute("insert into test values(%s,%s,%s,%s,%s,%s)",values)
    db.commit()
    print(cursor.rowcount)

