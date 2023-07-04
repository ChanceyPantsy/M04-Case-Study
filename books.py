from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(120), unique=True)
    author = db.Column(db.String(120))
    publisher = db.Column(db.String(120))

    def __init__(self, book_name, author, publisher):
        self.book_name = book_name
        self.author = author
        self.publisher = publisher

@app.route('/book', methods=['POST'])
def add_book():
    book_name = request.json['book_name']
    author = request.json['author']
    publisher = request.json['publisher']

    new_book = Book(book_name, author, publisher)

    db.session.add(new_book)
    db.session.commit()

    return {
        'id': new_book.id,
        'book_name': new_book.book_name,
        'author': new_book.author,
        'publisher': new_book.publisher
    }

@app.route('/book', methods=['GET'])
def get_books():
    all_books = Book.query.all()
    return [book.to_dict() for book in all_books]

@app.route('/book/<id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    return {
        'id': book.id,
        'book_name': book.book_name,
        'author': book.author,
        'publisher': book.publisher
    }

@app.route('/book/<id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)

    book.book_name = request.json['book_name']
    book.author = request.json['author']
    book.publisher = request.json['publisher']

    db.session.commit()

    return {
        'id': book.id,
        'book_name': book.book_name,
        'author': book.author,
        'publisher': book.publisher
    }

@app.route('/book/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()

    return {
        'id': book.id,
        'book_name': book.book_name,
        'author': book.author,
        'publisher': book.publisher
    }

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
