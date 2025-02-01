import pyodbc
from .Entries.entries_db import SERVER


def connect_to_db():
    try:
        connection = pyodbc.connect(
            r"DRIVER={ODBC Driver 18 for SQL Server};"
            f"SERVER={SERVER};"
            f"Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
        connection.autocommit = True
        print("Connection established successfully")
        return connection
    except Exception as e:
        print(f"Error from connection to database: {e}")
        return None, None


def create_tables():
    connection = connect_to_db()

    if connection:
        cursor = connection.cursor()
        cursor.execute(
            "IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'SelectedBooks') BEGIN CREATE DATABASE SelectedBooks END"
        )

        cursor.execute("USE SelectedBooks;")

        cursor.execute(
            """IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Users')
            BEGIN
            CREATE TABLE Users (
                        UserID INT IDENTITY(1,1) PRIMARY KEY,
                        Login varchar(50) UNIQUE,
                        Password varchar(255) NOT NULL
                        )
                    END"""
        )

        cursor.execute(
            """ IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'WishListBooks')
            BEGIN
            CREATE TABLE WishListBooks (
                       
                        BookID INT IDENTITY(1,1) PRIMARY KEY,
                        Title nvarchar(255),
                        Author nvarchar(MAX),
                        Publisher nvarchar(255),
                        PublishedDate nvarchar(255),
                        Description nvarchar(MAX),
                        PageCount INT NOT NULL,
                        ImageLink nvarchar(2048), 
                        BuyLink nvarchar(2048),
                        Language nvarchar(10),


                        UserID INT FOREIGN KEY REFERENCES users(UserID),
                        DateAdded DATETIME DEFAULT GETDATE()
                    );
        
        END"""
        )


connection = connect_to_db()
cursor = connection.cursor()

if __name__ == "__main__":
    connect_to_db()
    create_tables()