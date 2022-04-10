import sqlite3 as sq

conn = sq.connect("user_info.db")
c = conn.cursor()

#c.execute("""CREATE TABLE USER(password VARCHAR(100), 
   # day_added VARCHAR(100), 
   # email VARCHAR(120), 
   # first_name VARCHAR(50), 
   # last_name VARCHAR(50), 
   # birthday VARCHAR(50), 
   # gender VARCHAR(50), 
   # phone_number VARCHAR(100), 
   # country VARCHAR(100));""")
#c.execute("""INSERT INTO USER VALUES('mypass19', '4/10/2022', 'example.com', 'John', 'Thies', '9/16/2002', 'male', '1837569434', 'Ecuador');""")
conn.commit()
c.close()