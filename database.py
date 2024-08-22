import sqlite3
from typing import List
import datetime
from model import Book

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('library.db')
c = conn.cursor()

# Function to create the table if it doesn't exist
def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS books (
            title text,
            author text,
            genre text,
            date_added text,
            date_read text,
            status integer,
            position integer
            )""")

create_table()

# Function to insert a new book into the database
def insert_book(book: Book):
    c.execute('select count(*) FROM books')
    count = c.fetchone()[0]
    book.position = count if count else 0
    with conn:
        c.execute('INSERT INTO books VALUES (:title, :author, :genre, :date_added, :date_read, :status, :position)',
        {'title': book.title, 'author': book.author, 'genre': book.genre, 
         'date_added': book.date_added, 'date_read': book.date_read, 
         'status': book.status, 'position': book.position })

# Function to retrieve all books from the database
def get_all_books() -> List[Book]:
    c.execute('select * from books')
    results = c.fetchall()
    books = []
    for result in results:
        books.append(Book(*result))
    return books

# Function to delete a book from the database
def delete_book(position):
    c.execute('select count(*) from books')
    count = c.fetchone()[0]

    with conn:
        c.execute("DELETE from books WHERE position=:position", {"position": position})
        for pos in range(position+1, count):
            change_position(pos, pos-1, False)

# Function to update the position of a book
def change_position(old_position: int, new_position: int, commit=True):
    c.execute('UPDATE books SET position = :position_new WHERE position = :position_old',
                {'position_old': old_position, 'position_new': new_position})
    if commit:
        conn.commit()

# Function to update a book's information in the database
def update_book(position: int, title: str = None, author: str = None, genre: str = None):
    with conn:
        if title is not None:
            c.execute('UPDATE books SET title = :title WHERE position = :position',
                      {'position': position, 'title': title})
        if author is not None:
            c.execute('UPDATE books SET author = :author WHERE position = :position',
                      {'position': position, 'author': author})
        if genre is not None:
            c.execute('UPDATE books SET genre = :genre WHERE position = :position',
                      {'position': position, 'genre': genre})

# Function to mark a book as read in the database
def mark_read(position: int):
    with conn:
        c.execute('UPDATE books SET status = 2, date_read = :date_read WHERE position = :position',
                  {'position': position, 'date_read': datetime.datetime.now().isoformat()})
