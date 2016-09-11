from app import app
from flask import request
from flask_json import as_json

from app.models.user import User
from app.models.review import Review
from app.models.review_user import ReviewUser
from app.models.review_place import ReviewPlace
from app.models.place import Place
from app.views.return_styles import ListStyle

'''receives post data for reviews and returns a dict'''
def review_dict(message, from_user_id, stars):
	values = {
		'message': message,
		'user': int(from_user_id),
	}
	if stars != None:
		values['stars'] = int(stars)
	return values

'''GET: gets all reviews a user has received with pagination <url/users/user_id/reviews>'''
'''listing endpoint'''
@app.route('/users/<int:user_id>/reviews', methods=['GET'])
@as_json
def get_reviews(user_id):
	query = Review.select().join(ReviewUser).where(ReviewUser.user == user_id)
	return ListStyle.list(query,request)

'''POST: creates a new review for a user, the user's user_id to which the review is being posted must be mentioned in the URL <url/users/user_id/reviews>'''
@app.route('/users/<int:user_id>/reviews', methods=['POST'])
@as_json
def post_review(user_id):
    post_data = request.values
    if 'message' not in post_data or 'user_id' not in post_data:
    	return {"code": 400, "msg":"bad request, incomplete parameters"}, 400
    try:
    	user_to_query = User.get(User.id == user_id)
    except:
    	return {"code": 404, "msg":"to_user does not exist"}, 404

    review_dictionary = review_dict(
    	post_data['message'],
    	post_data['user_id'],
    	post_data.get('stars'),
    )

    new_review, created = Review.create_or_get(**review_dictionary)
    if not created:
    	return {"code": 404, "msg":"from_user does not exist"}, 404
    new_reviewUser, created = ReviewUser.create_or_get(
    	user = user_id,
    	review = new_review,
    )
    if not created:
    	return {"code": 404, "msg":"bad request"}, 404
    return new_review.to_dict()

'''GET: gets a single review, identified by review_id, of a user <url/users/user_id/reviews/review_id>'''
@app.route('/users/<int:user_id>/reviews/<int:review_id>', methods=['GET'])
@as_json
def get_review(user_id, review_id):
	try:
		rev_query = Review.select().join(ReviewUser).where(ReviewUser.user_id == user_id, Review.id == review_id).get()
	except:
		return {"code": 404, "msg":"There are no reviews for this user"}, 404
	return rev_query.to_dict()

'''DELETE: deletes a review, identified by review_id, received by a user <url/users/user_id/reviews/review_id>'''
@app.route('/users/<int:user_id>/reviews/<int:review_id>', methods=['DELETE'])
@as_json
def delete_review(user_id, review_id):
	try:
		rev_query2 = ReviewUser.select().where(ReviewUser.user == user_id, ReviewUser.review == review_id).get()
		rev_query = Review.select().join(ReviewUser).where(ReviewUser.user == user_id, Review.id == review_id).get()
	except:
		return {"code": 400, "msg":"Bad request"}, 400
	out_dict = rev_query.to_dict()
	rev_query2.delete_instance()
	rev_query.delete_instance()
	return out_dict

'''GET: gets all reviews a place has received with pagination <url/places/place_id/reviews>'''
'''listing endpoint'''
@app.route('/places/<int:place_id>/reviews', methods=['GET'])
@as_json
def get_reviews_by_place(place_id):
	query = Review.select().join(ReviewPlace).where(ReviewPlace.place == place_id)
	return ListStyle.list(query,request)

'''POST: creates a new review for a place, the place's place_id to which the review is being posted must be mentioned in the URL <url/places/place_id/reviews>'''
@app.route('/places/<int:place_id>/reviews', methods=['POST'])
@as_json
def post_review_by_place(place_id):
	post_data = request.values
	if 'message' not in post_data or 'user_id' not in post_data:
		return {"code": 400, "msg":"bad request, incomplete parameters"}, 400
	try:
		place_get = Place.get(Place.id == place_id)
	except Place.DoesNotExist:
		return {'code': 10004, 'msg': 'Place does not exist'}, 404
	review_dictionary = review_dict(
    	post_data['message'],
    	post_data['user_id'],
    	post_data.get('stars'),
    )

	new_review, created = Review.create_or_get(**review_dictionary)
	if not created:
		return {'code': 404, 'msg': 'User does not exist'}, 404
	new_review_place = ReviewPlace.create(place=place_id, review=new_review)
	return new_review.to_dict()

'''GET: gets a single review, identified by review_id, of a place <url/places/place_id/reviews/review_id>'''
@app.route('/places/<int:place_id>/reviews/<int:review_id>', methods=['GET'])
@as_json
def get_all_reviews_by_place(place_id, review_id):
	try:
		review_query = Review.select().join(ReviewPlace).where(ReviewPlace.place == place_id, Review.id == review_id).get()
	except:
		return {'code': 10004, 'msg': 'Place does not exist'}, 400
	return review_query.to_dict()

'''DELETE: deletes a review, identified by review_id, of a place <url/places/place_id/reviews/review_id>'''
@app.route('/places/<int:place_id>/reviews/<int:review_id>', methods=['DELETE'])
@as_json
def delete_all_reviews_by_place(place_id, review_id):
	try:
		query = ReviewPlace.select().where(ReviewPlace.place == place_id).get()
		review_query = Review.select().join(ReviewPlace).where(ReviewPlace.place == place_id, Review.id == review_id).get()
	except:
		return {'code': 400, 'msg': 'Bad Request'}, 400
    
	out_dict = review_query.to_dict()
	query.delete_instance()
	review_query.delete_instance()
	return out_dict

