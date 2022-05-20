CREATE DATABASE Userinfo;
USE UserInfo;

CREATE TABLE Users(
    UserID INTEGER,
    Username VARCHAR(50) NOT NULL,
    Pass VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    Phone_Number INTEGER NOT NULL,
    Gender VARCHAR(10) NOT NULL,
    Date_added VARCHAR(20) NOT NULL,
    Is_Admin BOOLEAN NOT NULL,
    Can_Post BOOLEAN NOT NULL,
    Is_Banned BOOLEAN NOT NULL,
    First_Name VARCHAR(50) NOT NULL,
    Last_Name VARCHAR(50) NOT NULL,
    Birthday VARCHAR(20) NOT NULL,
    Address VARCHAR(100) NOT NULL,
    User_Description VARCHAR(1000),
    Blocked_Users VARCHAR(1000),
    PRIMARY KEY(UserID),
    CONSTRAINT User_Identifier UNIQUE(UserID));

CREATE TABLE Public_Posts(
    PostID INTEGER,
    UserID INTEGER NOT NULL,
    Message VARCHAR(1000) NOT NULL,
    Date_Posted VARCHAR(20) NOT NULL,
    Is_Deleted BOOLEAN NOT NULL,
    Date_Edited VARCHAR(20),
    Edited_Message  VARCHAR(1000),
    PRIMARY KEY(PostID),
    CONSTRAINT Post_Identifier UNIQUE(PostID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID));

CREATE TABLE Client_Logs(
    LogID INTEGER,
    UserID INTEGER NOT NULL,
    Date_Logged_On VARCHAR(20) NOT NULL,
    PRIMARY KEY(LogID),
    CONSTRAINT Login UNIQUE(LogID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID));

CREATE TABLE Log_Outs(
    Log_Out_Id INTEGER,
    LogID INTEGER NOT NULL,
    Date_Logged_Out VARCHAR(20) NOT NULL,
    Logged_OUT_Or_Dropped_Off VARCHAR(20) NOT NULL,
    PRIMARY KEY(Log_Out_Id),
    CONSTRAINT Logout UNIQUE(Log_Out_Id),
    FOREIGN KEY (LogID) REFERENCES Client_Logs(LogID));

CREATE TABLE Private_Messages(
    MessageID INTEGER,
    UserID INTEGER NOT NULL,
    Receiver INTEGER NOT NULL,
    Message VARCHAR(1000) NOT NULL,
    Message_Date VARCHAR(20) NOT NULL,
    Is_Deleted BOOLEAN NOT NULL,
    Date_Edited VARCHAR(20),
    Edited_Message VARCHAR(1000) NOT NULL,
    PRIMARY KEY (MessageID),
    CONSTRAINT Private_msg UNIQUE(MessageID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID));
