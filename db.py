import pdb
import psycopg2
import json
import os
import urllib.parse as up


url = os.environ['DATABASE_URL']

# pdb.set_trace()

conn = psycopg2.connect(url,sslmode='require')

user_table = 'telegramUsers'
prod_table = 'products'
order_table = 'orders'

class User:
    def __init__(self,conn=conn):
        self.conn = conn
        self.cur = self.conn.cursor()
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {user_table} (chatId INTEGER PRIMARY KEY, history JSONB)")
        self.conn.commit()  

    def insert(self,chatId,history):
        self.cur.execute(f"INSERT INTO {user_table} VALUES(%s, %s) ON CONFLICT DO NOTHING", (chatId, json.dumps(history),))
        self.conn.commit()


    def view(self):
        self.cur.execute(f"SELECT * FROM {user_table}")
        rows = self.cur.fetchall()
        return rows


    def delete(self,chatId):
        self.cur.execute(f"DELETE FROM {user_table} WHERE chatId = %s", (chatId,))
        self.conn.commit()


    def update(self,chatId,history):
        self.cur.execute(f"UPDATE {user_table} SET history = %s WHERE chatId = %s", (json.dumps(history), chatId,))
        self.conn.commit()

    def find(self,chatId):
        self.cur.execute(f"SELECT * FROM {user_table} WHERE chatId = %s",(chatId,))
        return self.cur.fetchone()


class Product:
    def __init__(self,conn=conn):
        self.conn = conn
        self.cur = self.conn.cursor()
        self.cur.execute(f'''CREATE TABLE IF NOT EXISTS "{prod_table}" (
    "comp_name" VARCHAR(50) NOT NULL,
    "prod_name" VARCHAR(50) NOT NULL,
    "prod_prep" VARCHAR(50) NOT NULL,
    "prod_brand" VARCHAR(50) NOT NULL,
    "prod_country" VARCHAR(50) NOT NULL,
    "price" VARCHAR(50) NOT NULL,
    "exp_date" VARCHAR(50) NOT NULL,
    "description" VARCHAR(400) NOT NULL,
    "stock_amount" VARCHAR(400),
    "chat_id" INT NOT NULL ,
    "verified" INT DEFAULT 0,
    "ID" SERIAL PRIMARY KEY
);''')
        self.conn.commit()  

    def insert(self,history,chatId):
        # pdb.set_trace()
        self.cur.execute(f"INSERT INTO {prod_table} VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING", (history[0],history[1],history[2],history[3],history[4],history[5],history[6],history[7],history[8],chatId,))
        self.cur.execute('SELECT LASTVAL()')
        lastid = self.cur.fetchone()[0]
        self.conn.commit()
        return lastid

    def view(self):
        self.cur.execute(f"SELECT * FROM {prod_table}")
        rows = self.cur.fetchall()
        return rows

    def viewOne(self,id):
        self.cur.execute(f'SELECT * FROM {prod_table} WHERE "ID"=%s',(id,))
        return self.cur.fetchone()

    def delete(self,id):
        self.cur.execute(f'DELETE FROM {prod_table} WHERE "ID" = %s', (id,))
        self.conn.commit()

    def verify(self,id):
        self.cur.execute(f'UPDATE {prod_table} SET verified = 1 WHERE "ID" = %s', (id,))
        self.conn.commit()


    # def update(self,chatId,history):
    #     self.cur.execute(f"UPDATE {prod_table} SET history = %s WHERE chatId = %s", (json.dumps(history), chatId,))
    #     self.conn.commit()


class Order:
    def __init__(self,conn=conn):
        self.conn = conn
        self.cur = self.conn.cursor()
        self.cur.execute(f'''CREATE TABLE IF NOT EXISTS "orders" (
    "chat_id" INT NOT NULL,
    "prod_id" INT NOT NULL,
    "ID" SERIAL PRIMARY KEY
);''')
        self.conn.commit()  

    def insert(self,chatId,prod_id):
        self.cur.execute(f"INSERT INTO {order_table} VALUES(%s, %s) ON CONFLICT DO NOTHING", (chatId,prod_id,))
        self.conn.commit()


    def view(self):
        self.cur.execute(f"SELECT * FROM {order_table}")
        rows = self.cur.fetchall()
        return rows

    def viewOne(self,id):
        self.cur.execute(f"SELECT * FROM {order_table} WHERE ID=%s",(id,))
        return self.cur.fetchone()

    def delete(self,id):
        self.cur.execute(f"DELETE FROM {order_table} WHERE id = %s", (id,))
        self.conn.commit()