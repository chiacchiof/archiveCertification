import pymysql
import time

conn = pymysql.connect(host='127.0.0.1', user='root', password='entra123', db='testDB')
cur = conn.cursor()
while True:
    cur.execute("SELECT * FROM transactions")
    for response in cur:
        print(response)
        conn.commit()
    time.sleep(5)
    
cur.close()
conn.close()
