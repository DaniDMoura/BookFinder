# BookFinder


BookFinder is a desktop application built with Python and ttkbootstrap that allows users to search for books using the Google Books API. Users can create accounts, search for books, view detailed information about them, and maintain a wishlist of their favorite books.


<p align="center">
  <img src="assets/Images/research.PNG" width="200" />
</p>


## Features


- User authentication system with secure password hashing
- Book search functionality using Google Books API
- Detailed book information display including:

  - Title and Author
  - Publisher and Publication Date
  - Description
  - Page Count
  - Language
  - Cover Image
  - Buy Link (when available)
- Personal wishlist management
- Modern dark theme UI using ttkbootstrap

## Prerequisites

- Python 3.8+
- SQL Server
- ODBC Driver 18 for SQL Server
- Google Books API Key

## Installation


1. Clone the repository:

```bash
git clone https://github.com/DaniDMoura/BookFinder.git
cd BookFinder
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory using the `.env.example` as template:
```env
API_KEY=your_google_books_api_key
SERVER_URL=your_sql_server_url
```

4. Set up the database:

   - Use the SQL scripts in the `db_queries` folder to create the necessary database and tables
   - Run `create_database.sql` first to create the SelectedBooks database
   - Then run `create_tables.sql` to create the Users and WishListBooks tables

## Project Structure

```
BookFinder/
├── assets/
│   ├── Icons/
│   │   └── (application icons)
│   └── Images/
│       └── (application images)
├── db_queries/
│   ├── create_database.sql
│   └── create_tables.sql
├── scripts/
│   ├── __init__.py
│   ├── auth.py
│   ├── config.py
│   ├── crud.py
│   ├── db_connection.py
│   ├── main.py
│   └── requestdata.py
├── .env.example
├── .gitignore
├── LICENSE.txt
├── README.md
└── requirements.txt
```

## Configuration

### Google Books API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Google Books API
4. Create credentials (API key)
5. Add your API key to the `.env` file

### SQL Server
1. Install SQL Server
2. Install ODBC Driver 18 for SQL Server
3. Add your server URL to the `.env` file
4. Run the database scripts from the `db_queries` folder

## Usage

1. Run the application:
```bash
python -m scripts.main
```

2. Create a new account or sign in with existing credentials

3. Search for books using the search bar

4. Click on book covers to view detailed information

5. Add books to your wishlist using the "Put this book on my wish list" button

6. View your wishlist using the "See your wish list" button

## Security Features

- Password hashing using bcrypt
- Input validation for usernames and passwords
- SQL injection prevention using parameterized queries
- Secure database connections

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details

## Acknowledgments

- [Google Books API](https://developers.google.com/books)
- [ttkbootstrap](https://ttkbootstrap.readthedocs.io/)
- [pyodbc](https://github.com/mkleehammer/pyodbc)
- [bcrypt](https://github.com/pyca/bcrypt/)

## Contact

Project Link: [https://github.com/DaniDMoura/BookFinder](https://github.com/DaniDMoura/BookFinder)