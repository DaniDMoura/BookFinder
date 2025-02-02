USE LivrosSelecionados;
GO

CREATE TABLE Users
(
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    Login varchar(50) UNIQUE,
    Password varchar(255) NOT NULL,
    Name varchar(255) NOT NULL
)

CREATE TABLE WishListBooks
(

    BookID INT IDENTITY(1,1) PRIMARY KEY,
    Title nvarchar(255) NOT NULL,
    Author nvarchar(MAX) NOT NULL,
    Publisher nvarchar(255) NOT NULL,
    PublishedDate nvarchar(255) NOT NULL,
    Description nvarchar(MAX) NOT NULL,
    PageCount INT NOT NULL,
    ImageLink nvarchar(2048), 
    BuyLink nvarchar(2048),
    Language nvarchar(10) NOT NULL,                     
    UserID INT FOREIGN KEY REFERENCES users(UserID),
    DateAdded DATETIME DEFAULT GETDATE()
);
GO

