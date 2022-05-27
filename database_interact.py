"""
This module can be used to interact with the database to insert,
select, or update data.
"""


#These are the imports needed for the functions defined in this module
#to work propertly. This module has been mainly designed to allow the
#functions to be imported into other projects. Thus, the following
#modules will need to be imported into any project the functions
#defined in this module are used in.
import mysql.connector
from datetime import datetime
#######################################

def table_counter(table_name: str):
    #This function is used to get the number of rows there are in a given table
    #When the number of rows are known, we can use the next number higher number
    #to make a unique ID that has not already been used.
    data,c = database_interact()
    c.execute(f"SELECT COUNT(*) FROM {table_name};")
    ID = c.fetchone()
    data.commit()
    c.close()
    return ID


def database_interact():
    #This function is used to make the connecting processs in other functions quicker to write.
    #Instead of defining the following lines of code in every function, this function only needs
    #to be called and stored in two variables.
    data = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="special")
    c = data.cursor(buffered=True)
    c.execute("USE Userinfo")
    return (data, c)


def add_user(username: str , password: str , email: str, phone_number: int, gender: str, first_name: str, last_name: str, birthday: str, address: str):
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
    data, c = database_interact()
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


def login_user(username: str, password: str):
    data,c = database_interact()
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
    ID = table_counter("Client_Logs")
    logged_in_date = datetime.now()
    data, c = database_interact()  
    try:
        c.execute(f"INSERT INTO Client_Logs VALUES({ID[0]+1}, '{user}', '{logged_in_date}', NULL, NULL);")
        data.commit()
        c.close()
        return ID
    except mysql.connector.errors.IntegrityError:
        return "Falied: Username is not in Database"


def logout_session(log_ID, logged_or_dropped):
    Logged_Out = datetime.now()
    data,c = database_interact()
    c.execute(f"""UPDATE Client_Logs SET 
        Date_Logged_Out = '{Logged_Out}', 
        Logged_Out_Or_Dropped_Off = '{logged_or_dropped}' 
        WHERE ID = {log_ID};""")
    data.commit()
    c.close()
    return "Successful!"


def get_public_post():
    data, c = database_interact()
    c.execute("SELECT Username, Msg, Date_Posted FROM Public_Posts WHERE Is_Deleted = False;")
    message = c.fetchall()
    data.close()
    return message


def inserting_post(msg, author):
    time = datetime.now()
    ID = table_counter("Public_Posts")
    data,c = database_interact()
    try:
        c.execute(f"INSERT INTO Public_Posts VALUES('{ID[0]+1}', '{author}', '{msg}', '{time}', False);")
    except mysql.connector.errors.IntegrityError:
        return "Failed: Not a vaild username!"
    data.commit()
    c.close()
    return "Successful!"


def inserting_private_msg(user, recv, msg):
    time = datetime.now()
    ID = table_counter("Private_Messages")
    data,c = database_interact()
    try:
        c.execute(f"INSERT INTO Private_Messages VALUES({ID[0]+1}, '{user}', '{recv}', '{msg}', '{time}', False);")
        data.commit()
        c.close()
    except mysql.connector.errors.IntegrityError:
        return "Failed: Not a vailid user!"
    return "Successful"


#the following code can be used to test the functions above
#print(login_session("Brandon")[0])
#print(logout_session(1, "Dropped off"))
#print(get_public_post())
#print(inserting_private_msg("Brandon", "Sam", "This is a test!"))
#print(add_user("Izzy", "brandpass", "brandmail", 103944, "Male", "Brandon", "Thies", "05-25-2002", "Lazy Lane 83728"))
#print(add_user("Russell", "brandpass", "brandmail", 103944, "Male", "Brandon", "Thies", "05-25-2002", "Lazy Lane 83728"))
#print(inserting_post("This is a test!", "Brandon"))