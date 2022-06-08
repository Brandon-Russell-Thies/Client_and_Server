"""
This module can be used to interact with the database to insert,
select, or update data.
"""


class Database:
    def __init__(self):
        import mysql.connector
        from datetime import datetime
        self.datetime = datetime
        self.mysql = mysql
        #This function is used to make the connecting processs in other functions quicker to write.
        #Instead of defining the following lines of code in every function, this function only needs
        #to be called and stored in two variables.
        self.data = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="special")
        self.c = self.data.cursor(buffered=True)
        self.c.execute("USE Userinfo")


    def table_counter(self, table_name: str):
        #This function is used to get the number of rows there are in a given table
        #When the number of rows are known, we can use the next highest number
        #to make a unique ID that has not already been used.
        
        self.c.execute(f"SELECT COUNT(*) FROM {table_name};")
        ID = self.c.fetchone()
        self.data.commit()
        return ID[0]


    def add_user(self, username: str , password: str , email: str, phone_number: int, gender: str, first_name: str, last_name: str, birthday: str, address: str):
        date_added = self.datetime.now()
        is_admin = False
        can_post = True
        is_banned = False

        if len(username) == 0 or len(password) == 0 or len(first_name) == 0 or len(last_name) == 0 or len(address) == 0:
            return "Failed: Please finish filling out all the information."
        try:
            birthday = self.datetime.strptime(birthday, '%m-%d-%Y').date()#Example of a valid date: 09-16-2002
        except ValueError:
            return "Failed: not a valid date"
        if gender != "Male" and gender != "Female":
            return "Failed: Please input 'Male', or 'Female' as your gender." 
        try:
            self.c.execute(f"""INSERT INTO Users VALUES(
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
        except self.mysql.connector.errors.IntegrityError:
            return "Failed: This username already exists!"
        self.data.commit()
        return "Successful"


    def login_user(self, username: str, password: str):
        #if username == "*" or password == "*":
            #return "Failed: Hackers are not aloud!"
        self.c.execute(f"SELECT Username, pass FROM Users WHERE Username = '{username}';")
        user = self.c.fetchone()
        print(user)
        self.data.commit()
        if user == None:
            return "Failed: Username does not exist!"
        if user[1] != password:
            return "Failed: Incorrect password!"
        return "Succussful"


    def login_session(self, user):
        ID = self.table_counter("Client_Logs")
        logged_in_date = self.datetime.now()  
        try:
            self.c.execute(f"INSERT INTO Client_Logs VALUES({ID+1}, '{user}', '{logged_in_date}', NULL, NULL);")
            self.data.commit()
            return ID
        except self.mysql.connector.errors.IntegrityError:
            return "Falied: Username is not in Database"


    def logout_session(self, log_ID, logged_or_dropped):
        Logged_Out = self.datetime.now()
        self.c.execute(f"""UPDATE Client_Logs SET 
            Date_Logged_Out = '{Logged_Out}', 
            Logged_Out_Or_Dropped_Off = '{logged_or_dropped}' 
            WHERE ID = {log_ID};""")
        self.data.commit()
        return "Successful!"


    def get_public_post(self):
        self.c.execute("SELECT Username, Msg, Date_Posted FROM Public_Posts WHERE Is_Deleted = False;")
        message = self.c.fetchall()
        return message


    def inserting_post(self, msg, author):
        time = self.datetime.now()
        ID = self.table_counter("Public_Posts")
        try:
            self.c.execute(f"INSERT INTO Public_Posts VALUES('{ID[0]+1}', '{author}', '{msg}', '{time}', False);")
        except self.mysql.connector.errors.IntegrityError:
            return "Failed: Not a vaild username!"
        self.data.commit()
        return "Successful!"


    def inserting_private_msg(self, user, recv, msg):
        time = self.datetime.now()
        ID = self.table_counter("Private_Messages")
        try:
            self.c.execute(f"INSERT INTO Private_Messages VALUES({ID+1}, '{user}', '{recv}', '{msg}', '{time}', False);")
            self.data.commit()
        except self.mysql.connector.errors.IntegrityError:
            return "Failed: Not a vailid user!"
        return "Successful"


    def get_private_msg(self, user: str, recv: str):
        self.c.execute(f"SELECT * FROM Private_Messages WHERE Username = '{user}' AND Receiver = '{recv}'")
        messages = self.c.fetchall()
        return messages

interactor = Database()
print(interactor.add_user("Ella", "brandpass", "brandmail", 103944, "Male", "Brandon", "Thies", "05-25-2002", "Lazy Lane 83728"))
print(interactor.inserting_private_msg("Brandon", "Izzy", "This is a test!"))
#print(interactor.get_public_post())

#print(login_session("Brandon")[0])
#print(logout_session(1, "Dropped off"))
#print(get_public_post())
#print(inserting_private_msg("Brandon", "Izzy", "This is a test!"))
#print(inserting_post("This is a test!", "Brandon"))
#print(get_private_msg("Brandon", "Izzy"))
