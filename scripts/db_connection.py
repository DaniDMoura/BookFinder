import pyodbc
from Entries.entries_db import SERVER


def connect_to_db():
    try:
        connection = pyodbc.connect(
            r"DRIVER={ODBC Driver 18 for SQL Server};"
            f"SERVER={SERVER};"
            f"Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
        connection.autocommit = True
        cursor = connection.cursor()
        print("Connection established successfully")
        return connection, cursor
    except Exception as e:
        print(f"Error from connection to database: {e}")
        return None, None


if __name__ == "__main__":
    connection, cursor = connect_to_db()

    if connection:
        cursor.execute(
            "IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'SelectedBooks') BEGIN CREATE DATABASE SelectedBooks END"
        )

        cursor.execute("USE SelectedBooks")

        cursor.execute(
            """IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Users')
            BEGIN
            CREATE TABLE Users (
                        UserID INT IDENTITY(1,1) PRIMARY KEY,
                        Login varchar(50) UNIQUE,
                        Password varchar(255) NOT NULL,
                        Name varchar(255) NOT NULL
                        )
                    END"""
        )

        cursor.execute(
            """ IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'WishListBooks')
            BEGIN
            CREATE TABLE WishListBooks (
                       
                        BookID INT IDENTITY(1,1) PRIMARY KEY,
                        Title nvarchar(255) NOT NULL,
                        Author nvarchar(MAX) NOT NULL,
                        Publisher nvarchar(255) NOT NULL,
                        PublishedDate nvarchar(255) NOT NULL,
                        Description nvarchar(MAX) NOT NULL,
                        Categories nvarchar(255) NOT NULL,
                        PageCount INT NOT NULL,
                        Language nvarchar(10) NOT NULL,


                        UserID INT FOREIGN KEY REFERENCES users(UserID),
                        DateAdded DATETIME DEFAULT GETDATE()
                    );
        
        END"""
        )
