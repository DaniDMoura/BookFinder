from db_connection import connect_to_db

def create(
    Title,
    Author,
    Publisher,
    PublishedDate,
    Description,
    Categories,
    PageCount,
    Language,
    UserID,
):
    connection, cursor = connect_to_db()
    if connection:
        try:
            cursor.execute(
                """
            INSERT INTO WishListBooks
            VALUES
            (?,?,?,?,?,?,?,?,?),
                """,
                (
                    Title,
                    Author,
                    Publisher,
                    PublishedDate,
                    Description,
                    Categories,
                    PageCount,
                    Language,
                    UserID,
                ),
            )
            return True
        except Exception as e:
            print(f"Error to read wish list: {e}")
            return False
        finally:
            cursor.close()
            connection.close()
    return False


def read():
    books = []
    connection, cursor = connect_to_db()
    if connection:
        try:
            cursor.execute(
                """
            SELECT wish.* FROM WishListBooks wish
            INNER JOIN Users U ON wish.UserID = U.UserID
        """
            )
            books = cursor.fetchall()
        except Exception as e:
            print(f"Error to read wish list: {e}")
        finally:
            cursor.close()
            connection.close()
    return books

def delete(BookID):
    connection, cursor = connect_to_db()
    if connection:
        try:
            cursor.execute(
                """
        DELETE FROM WishListBooks WHERE BookID = ?
    """,
                (BookID,),
            )
            return True
        except Exception as e:
            print(f"Error to delete book: {e}")
            return False

        finally:
            cursor.close()
            connection.close()
    return False
