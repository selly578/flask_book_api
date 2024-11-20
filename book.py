from flask import Blueprint,jsonify,request
from models import Book,db 
from utils import jwt_required 

book = Blueprint("book",__name__)

@book.get("")
@jwt_required
def books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

@book.get("/<int:id>")
@jwt_required
def onebook(id):
    book  = Book.query.get_or_404(id)
    return jsonify(book.to_dict())

@book.post("/")
@jwt_required
def add_book():
    data = request.get_json()

    required_key = ["title","author","publisher","year"]

    for key in required_key:
        if not key in data.keys():
            return jsonify(message=f"{key} missing"),400

    new_book = Book(
        title = data.get("title"),
        author = data.get("author"),
        publisher = data.get("publisher"),
        year = data.get("year"),
        stock = data.get("stock",0)
    )
    db.session.add(new_book)
    db.session.commit()

    return jsonify(new_book.to_dict()),201

@book.put("/<int:id>")
@jwt_required
def edit_book(id):
    data = request.get_json()
    book = Book.query.get_or_404(id)

    book.title = data.get("title",book.title)
    book.author = data.get("author",book.author)
    book.publisher = data.get("publisher",book.publisher)
    book.year = data.get("year",book.year)
    book.stock = data.get("stock",book.stock)

    db.session.commit()

    return jsonify(book.to_dict())

@book.delete("/<int:id>")
@jwt_required
def delete_book(id):
    book = Book.query.get_or_404(id)
    
    db.session.delete(book)
    db.session.commit()

    return jsonify(message="book deleted")


