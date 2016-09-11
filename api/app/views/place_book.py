from app.models.place_book import PlaceBook
from app.models.place import Place
from app.models.user import User
from flask_json import as_json
from flask import request
from app import app
from datetime import datetime, timedelta
from app.views.return_styles import ListStyle

'''receives post data for placebook and returns a dict'''
def placebook_dict(place_id, user_id = None, is_validated = None, date_start = None, number_nights = None):
    values = {
        'user': int(user_id),
        'place': place_id,
        'date_start': datetime.strptime(date_start, "%Y/%m/%d %H:%M:%S"),
    }
    if is_validated != None and is_validated.lower() == "true":
        values['is_validated'] = True
    if number_nights != None:
        values['number_nights'] = int(number_nights)
    else:
        values['number_nights'] = 1
    return values

'''GET: Gets all bookings for places with pagination <url/places/place_id/books>'''
'''listing endpoint'''
@app.route('/places/<int:place_id>/books', methods=['GET'])
@as_json
def get_place_books(place_id):
    query = PlaceBook.select().where(PlaceBook.place == place_id)
    return ListStyle.list(query,request)

'''POST: Create a new booking for a place <url/places/place_id/books>'''
@app.route('/places/<int:place_id>/books', methods=['POST'])
@as_json
def book_place(place_id):
    post_data = request.values
    keys=["user_id", "date_start"]
    for key in keys:
        if key not in post_data:
            return {"code":400, "msg":"bad request"}, 404

    place_book_dictionary = placebook_dict(
        place_id,
        post_data['user_id'],
        post_data.get('is_validated'),
        post_data['date_start'],
        post_data.get('number_nights')
    )
    # check overlap
    query = PlaceBook.select().where(PlaceBook.place == place_id)
    new_book_end = place_book_dictionary['date_start'] + timedelta(days = place_book_dictionary['number_nights'])
    
    for booking in query:
        end_date = booking.date_start + timedelta(days=booking.number_nights)
        if  place_book_dictionary['date_start'].date() <= booking.date_start.date() <= new_book_end.date() or place_book_dictionary['date_start'].date() <= end_date.date() <= new_book_end.date():
            return {'code': 110000, 'msg': "Place unavailable at this date"}, 410
    # overlap check end

    new_book, created = PlaceBook.create_or_get(**place_book_dictionary)
    if not created:
        return {"code":400, "msg":"bad request"}, 404
    return new_book.to_dict()

'''GET: Gets a single booking for a plce <url/places/place_id/books/book_id>'''
@app.route('/places/<int:place_id>/books/<book_id>', methods=['GET'])
@as_json
def get_single_booking(place_id, book_id):
    try:
        get_booking = PlaceBook.get(PlaceBook.id == book_id, PlaceBook.place == place_id)
    except PlaceBook.DoesNotExist:
        return {"code":404, "msg":"not found"}, 404
    return get_booking.to_dict()

'''DELETE: Deletes a booking for a place <url/places/place_id/books/book_id>'''
@app.route('/places/<int:place_id>/books/<int:book_id>', methods=['DELETE'])
@as_json
def del_single_book(place_id, book_id):
    try:
        query = PlaceBook.get(PlaceBook.id == book_id)
    except PlaceBook.DoesNotExist:
        return {"code":404, "msg":"not found"}, 404
    out_dict = query.to_dict()
    query.delete_instance()
    return out_dict

'''PUT: Changes data for an existing booking <url/places/places_id/books/book_id>'''
@app.route('/places/<int:place_id>/books/<int:book_id>', methods=['PUT'])
@as_json
def change_book(place_id, book_id):
    post_data = request.values
    try:
        query = PlaceBook.get(PlaceBook.id == book_id)
    except PlaceBook.DoesNotExist:
        return {"code":404, "msg":"not found"}, 404
    
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
    return query.to_dict()

