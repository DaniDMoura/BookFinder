from .db_connection import connect_to_db
from .auth import Authentication
from contextlib import contextmanager




@contextmanager
def get_db_connection():
    try:
        connection = connect_to_db()
        yield connection
    except Exception as e:
        print(f"Database connection error: {e}")
        raise
    finally:
        if connection:
            try:
                connection.close()
            except Exception as e:
                print(f"Error closing connection: {e}")

def create(
    Title,
    Author,
    Publisher,
    PublishedDate,
    Description,
    PageCount,
    Language,
    ImageLink,
    BuyLink,
    user_id
):
    with get_db_connection() as connection:

        try:
            cursor = connection.cursor()
            cursor.execute("USE SelectedBooks;")
            cursor.execute(
                """
            INSERT INTO WishListBooks (Title, 
            Author, 
            Publisher, 
            PublishedDate, 
            Description, 
            PageCount, 
            Language, 
            ImageLink, 
            BuyLink, 
            UserID)
            VALUES
            (?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    Title,
                    Author,
                    Publisher,
                    PublishedDate,
                    Description,
                    PageCount,
                    Language,
                    ImageLink,
                    BuyLink,
                    user_id
                ),
            )
            return True
        except Exception as e:
            print(f"Error adding book to wishlist: {e}")
            return False
        finally:
            cursor.close()
    return False


def read(user_id):
    books = []
    connection = connect_to_db()
    cursor = connection.cursor()
    if connection:
        try:
            cursor.execute("USE SelectedBooks;")
            cursor.execute(
                """
            SELECT * FROM WishListBooks 
            WHERE UserID = ?
        """,(user_id,)
            )
            books = cursor.fetchall()
        except Exception as e:
            print(f"Error to read wish list: {e}")
        finally:
            cursor.close()
            connection.close()
    return books


def delete(book_id,user_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    if connection:
        try:
            cursor.execute("USE SelectedBooks;")
            cursor.execute(
                """
        DELETE FROM WishListBooks WHERE BookID = ? AND UserID = ?
    """,
                (book_id,user_id),
            )
            return True
        except Exception as e:
            print(f"Error to delete book: {e}")
            return False

        finally:
            cursor.close()
            connection.close()
    return False
