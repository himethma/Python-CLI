import typer
from rich.console import Console
from rich.table import Table
from model import Book
from database import get_all_books, delete_book, insert_book, mark_read, update_book

console = Console()

app = typer.Typer()

@app.command(short_help='adds a book')
def add(title: str, author: str, genre: str):
    typer.echo(f"Adding {title} by {author} in {genre} genre")
    book = Book(title, author, genre)
    insert_book(book)
    show()

@app.command()
def delete(position: int):
    typer.echo(f"Deleting book at position {position}")
    delete_book(position-1)
    show()

@app.command()
def update(position: int, title: str = None, author: str = None, genre: str = None):
    typer.echo(f"Updating book at position {position}")
    update_book(position-1, title, author, genre)
    show()

@app.command()
def mark_as_read(position: int):
    typer.echo(f"Marking book at position {position} as read")
    mark_read(position-1)
    show()

@app.command()
def show():
    books = get_all_books()
    console.print("[bold magenta]Library[/bold magenta]!", "📚")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Title", min_width=20)
    table.add_column("Author", min_width=20)
    table.add_column("Genre", min_width=12, justify="right")
    table.add_column("Read", min_width=12, justify="right")

    def get_genre_color(genre):
        COLORS = {'Fiction': 'cyan', 'Non-Fiction': 'green', 'Fantasy': 'purple', 'Science': 'blue'}
        if genre in COLORS:
            return COLORS[genre]
        return 'white'

    for idx, book in enumerate(books, start=1):
        c = get_genre_color(book.genre)
        is_read_str = '✅' if book.status == 2 else '❌'
        table.add_row(str(idx), book.title, book.author, f'[{c}]{book.genre}[/{c}]', is_read_str)
    console.print(table)


if __name__ == "__main__":
    app()
