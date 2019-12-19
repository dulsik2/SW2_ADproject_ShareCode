# database connection 을 위한 라이브러리
import sys, pymysql

class Sql:
    def __init__(self):
        self.sqlConnect()

    def sqlConnect(self):
        try:
            self.conn = pymysql.connect(
                host='3.16.130.134',
                user='root',
                password='1234',
                db='swproject2_db',
                port=3306,
                charset='utf8',
            )
        except Exception as e:
            print("문제가 있네요! : ", type(e))
            exit(1)
        print("연결 성공!")
        self.cur = self.conn.cursor()

    def select(self, query):
        self.cur.execute(query)
        self.conn.commit()
        rs = self.cur.fetchall()
        return rs

    def insert(self, query):
        self.cur.execute(query)
        self.conn.commit()

    def insert_b(self, query, data):
        try:
            self.cur.execute(query, data)
            self.conn.commit()
        except Exception as e:
            print(e)

    def delete(self, query):
        self.cur.execute(query)
        self.conn.commit()

    def update(self, query):
        self.cur.execute(query)
        self.conn.commit()

    def update_b(self, query, data):
        self.cur.execute(query, data)
        self.conn.commit()

if __name__  == "__main__":
    sql = Sql()
    rs = sql.select("select * from member;")

    for i in range(len(rs)):
        print(rs[i])

