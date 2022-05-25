import mysql.connector
from datetime import datetime


def add_user(username: str , password: str , email: str, phone_number: int, gender: str, first_name: str, last_name: str, birthday: str, address: str):
    data = mysql.connector.connect(
    host="localhost", 
    user="root", 
    passwd="special")
    c = data.cursor()

    date_added = datetime.now()
    is_admin = False
    can_post = True
    is_banned = False

    if len(username) == 0 or len(password) == 0 or len(first_name) == 0 or len(last_name) == 0 or len(address) == 0:
        return "Failed: Please finish filling out all the information."
    try:
        birthday = datetime.strptime(birthday, '%m-%d-%Y').date()#Example of a valid date: 09-16-2002
    except ValueError:
        return "Failed: not a valid date"
    
    if gender != "Male" and gender != "Female":
        return "Failed: Please input 'Male', or 'Female' as your gender." 
    
    c.execute("USE Userinfo;")
    try:
        c.execute(f"""INSERT INTO Users VALUES(
            '{username}',
            '{password}',
            '{email}',
            {phone_number},
            '{gender}','
            {date_added}',
            {is_admin},
            {can_post},
            {is_banned},
            '{first_name}',
            '{last_name}',
            '{birthday}',
            '{address}', 
            NULL);""")
    except mysql.connector.errors.IntegrityError:
        return "Failed: This username already exists!"

    c.close()
    data.commit()

    return "Successful"

#print(add_user("Brandon", "brandpass", "brandmail", 103944, "Male", "Brandon", "Thies", "05-25-2002", "Lazy Lane 83728"))

def login_user(username: str, password: str):

    data = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="special"
    )
    c = data.cursor(buffered=True)
    c.execute("USE Userinfo;")
    c.execute(f"SELECT Username, pass FROM Users WHERE Username = '{username}';")
    user = c.fetchone()
    c.close()
    data.commit()
    if user == None:
        return "Failed: Username does not exist!"
    if user[1] != password:
        return "Failed: Incorrect password!"
    return "Succussful"



def login_session(user):
    #The following lines of code works to get the number of logs in the database
    #the program will then add one more to the count and make that be the new log ID
    data = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="special"
    )
    c = data.cursor(buffered=True)
    c.execute("USE Userinfo")

    c.execute("SELECT COUNT(*) FROM Client_Logs;")
    ID = c.fetchone()
    
    data.commit()
    c.close()
    ###########################################

    logged_in_date = datetime.now()
    
    data = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="special"
    )
    c = data.cursor()
        
    try:
        c.execute("USE Userinfo")
        c.execute(f"INSERT INTO Client_Logs VALUES({ID[0]+1}, '{user}', '{logged_in_date}', NULL, NULL);")
        data.commit()
        c.close()
        return ID
    except mysql.connector.errors.IntegrityError:
        return "Falied: Username is not in Database"



def logout_session(log_ID, logged_or_dropped):

    Logged_Out = datetime.now()
    data = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="special"
    )
    c = data.cursor()
    c.execute("USE Userinfo;")
    c.execute(f"""UPDATE Client_Logs SET 
        Date_Logged_Out = '{Logged_Out}', 
        Logged_Out_Or_Dropped_Off = '{logged_or_dropped}' 
        WHERE ID = {log_ID};""")

    data.commit()
    c.close()

    return "Successful!"
            
#print(login_session("Brandon")[0])
#print(logout_session(1, "Dropped off"))

def get_public_post():

    data = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="special"
    )
    c = data.cursor(buffered=True)
    c.execute("USE Userinfo")
    c.execute("SELECT Username, Msg, Date_Posted FROM Public_Posts WHERE Is_Deleted = False;")
    message = c.fetchall()
    return message

#print(get_public_post())

def inserting_post(msg, author):
    time = datetime.now()
    data = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="special"
    )
    c = data.cursor(buffered=True)
    c.execute("USE Userinfo")

    c.execute("SELECT COUNT(*) FROM Public_Posts;")
    ID = c.fetchone()
    
    data.commit()
    c.close()

    data = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="special"
    )
    c = data.cursor()
    c.execute("USE Userinfo")
    try:
        c.execute(f"INSERT INTO Public_Posts VALUES('{ID[0]+1}', '{author}', '{msg}', '{time}', False);")
    except mysql.connector.errors.IntegrityError:
        return "Failed: Not a vaild username!"
    data.commit()
    c.close()

    return "Successful!"

print(inserting_post("This is a test!", "Brandon"))