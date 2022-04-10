import sqlite3 as sq

conn = sq.connect("./Client_and_Server/users.db")
c = conn.cursor()
#c.execute("""CREATE TABLE USERS(Name VARCHAR(100), is_banned VARCHAR(10));""")

#c.execute("INSERT INTO USERS VALUES('John_Thies', 'true')")
conn.commit()
