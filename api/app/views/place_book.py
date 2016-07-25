from app.models.place_book import PlaceBook
from app.models.place import Place
from app.models.user import User
from flask_json import as_json
from flask import request, jsonify
from app import app
from datetime import datetime

@app.route('/places/<int:place_id>/books', methods=['GET'])
def get_place_books(place_id):
    try:
        query = PlaceBook.select().where(PlaceBook.place == place_id)
    except:
        return {"code":404, "msg":"not found"}, 404
    place_books = []
    for place_book in query:
        place_books.append(place_book.to_hash())
    return jsonify(place_books)

@app.route('/places/<int:place_id>/books', methods=['POST'])
@as_json
def book_place(place_id):
    try:    
        post_data = request.values
        new = PlaceBook.create(
            place = place_id,
            user = post_data['user_id'],
            date_start = datetime.strptime(post_data['date_start'], "%Y/%m/%d %H:%M:%S")
        )
        if 'is_validated' in post_data:
            if post_data['is_validated'].lower() == 'true':
                new.is_validated = True
            elif post_data['is_validated'].lower() == 'false':
                new.is_validated = False
        if 'number_nights' in post_data:
            new.number_nights = int(post_data['number_nights'])
        new.save()
        return new.to_hash()
    except:
        return {"code":404, "msg":"not found"}, 404

@app.route('/places/<int:place_id>/books/<book_id>', methods=['GET'])
@as_json
def get_books(place_id, book_id):
    try:
        get_booking = PlaceBook.get(PlaceBook.id == book_id, PlaceBook.place == place_id)
        return get_booking.to_hash()
    except:
        return {"code":404, "msg":"not found"}, 404

@app.route('/places/<int:place_id>/books/<int:book_id>', methods=['DELETE'])
@as_json
def del_book(place_id, book_id):
    try:
        query = PlaceBook.get(PlaceBook.id == book_id)
    except:
        return {"code":404, "msg":"not found"}, 404
    out_dict = query.to_hash()
    query.delete_instance()
    return out_dict

@app.route('/places/<int:place_id>/books/<int:book_id>', methods=['PUT'])
@as_json
def change_book(place_id, book_id):
    try:
        query = PlaceBook.get(PlaceBook.id == book_id)
    except:
        return {"code":404, "msg":"not found"}, 404
    post_data = request.values
    for key in post_data:
        if key == 'is_validated':
            if post_data[key].lower() == 'true':
                query.is_validated = True
            elif post_data[key].lower() == 'false':
                query.is_validated = False
        if key == 'date_start':
            query.date_start = datetime.strptime(post_data[key], "%Y/%m/%d %H:%M:%S")
        if key == 'number_nights':
            query.number_nights = int(post_data[key])
    query.save()
    return query.to_hash()
