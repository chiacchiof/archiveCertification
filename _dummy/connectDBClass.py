import pymysql
import time


class InspectDB():
    def __init__(self):
        self._conn = pymysql.connect(host='127.0.0.1', user='root', password='entra123', db='testDB')
        self._cur = self._conn.cursor()

    def run(self):
        while True:
            self._cur.execute("SELECT * FROM transactions")
            time.sleep(5)
            for response in self._cur:
                print(response)
                self._conn.commit()
        cur.close()
        conn.close()

if __name__ == '__main__':
    InspectDB().run()
