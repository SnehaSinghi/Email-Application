import psycopg2

def createTable():
    conn = psycopg2.connect("dbname='postgres' user='postgres' password ='postgres123' host='localhost' port = '5432'")
    cur = conn.cursor()
    #cur.execute("CREATE EXTENSION pgcrypto;")
    cur.execute("CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY, email TEXT NOT NULL UNIQUE, password TEXT NOT NULL)")
    conn.commit()
    conn.close()
def insert():
    conn = psycopg2.connect("dbname='postgres' user='postgres' password ='postgres123' host='localhost' port = '5432'")
    cur = conn.cursor()
    #cur.execute("INSERT INTO store VALUES('%s', '%s', '%s')" %(item, quantity, price))
    cur.execute("INSERT INTO users (email, password) VALUES ('johndoe@mail.com', crypt('johnspassword', gen_salt('bf')))")
    #cur.execute("INSERT INTO accounts(username, "password) VALUES ('user2', 'pass2');")
    conn.commit()
    conn.close()
def view():
    conn = psycopg2.connect("dbname='postgres' user='postgres' password ='postgres123' host='localhost' port = '5432'")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    conn.close()
    return rows

def delete(item):
    conn = psycopg2.connect("dbname='postgres' user='postgres' password ='postgres123' host='localhost' port = '5432'")
    cur = conn.cursor()
    cur.execute("DELETE FROM store where item = %s", (item,))
    conn.commit()
    conn.close()

def update(quantity, price, item):
    conn = psycopg2.connect("dbname='postgres' user='postgres' password ='postgres123' host='localhost' port = '5432'")
    cur = conn.cursor()
    cur.execute("UPDATE store SET quantity = %s, price = %s WHERE item = %s",(quantity, price, item))
    conn.commit()
    conn.close()

createTable()
#insert("Water glass1",1010, 112)
#delete("Water glass")
#update(90, 100, "Wine glass")
print(view())
