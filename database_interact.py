


def add_user(username: str , password: str , email: str, phone_number: int, gender: str, first_name: str, last_name: str, birthday: str, address: str):
    import mysql.connector
    from datetime import datetime
    #imports are done inside of the functions to avoid issues when imported from another area

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
        birthday = datetime.strptime(birthday, '%m-%d-%Y').date()
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



def login_user(username: str, password: str):
    import mysql.connector

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
    
    
    


