from operator import lt
from flask import Blueprint,jsonify,request 
from models import Member,Book,Borrow,db
from utils import jwt_required
from datetime import date

member = Blueprint("member",__name__)

@member.get("")
@jwt_required
def members():
    members = Member.query.all()
    return jsonify([member.to_dict() for member in members])

@member.get("/<int:id>")
@jwt_required
def member_by_id(id):
    member = Member.query.get_or_404(id)
    return jsonify(member.to_dict())

@member.post("")
@jwt_required
def add_member():
    data = request.get_json()
    new_member = Member(
        name = data.get("name"),
        email = data.get("email"),
        address = data.get("address"),
        phone = data.get("phone"),
    )

    same_email = Member.query.filter_by(email=data.get("email")).first()

    if not same_email:
        db.session.add(new_member)
        db.session.commit()

        return jsonify(new_member)

    return jsonify(message="same email already exist")

@member.get("/borrow")
@jwt_required
def borrows():
    borrows = Borrow.query.all()
    return jsonify([borrow.to_dict() for borrow in borrows])

@member.post("/borrow")
@jwt_required
def borrow():
    data = request.get_json()

    member_id = data.get("member_id")
    book_id = data.get("book_id")

    member = Member.query.get(member_id)
    book = Book.query.get(book_id)

    if not member:
        return jsonify(message="Member not foud"),404

    if not book:
        return jsonify(message="Book not found"),404

    if book.stock < 1:
        return jsonify(message="Book out of stock"),400 

    new_borrow = Borrow(
       member_id = member_id,
       book_id = book_id, 
       borrow_date = date.today()
    )

    book.stock -= 1

    db.session.add(new_borrow)
    db.session.commit()

    return jsonify({"message": f"Book '{book.title}' borrowed successfully", "borrow_id": new_borrow.id}), 201

@member.post("/return/<int:borrow_id>")
@jwt_required
def return_book(borrow_id):
    borrow = Borrow.query.get_or_404(borrow_id)
    book = Book.query.get_or_404(borrow.book_id)

    borrow.return_date = date.today()
    book.stock += 1
    db.session.commit()

    return jsonify({"message": f"Book '{book.title}' returned successfully"}), 200
