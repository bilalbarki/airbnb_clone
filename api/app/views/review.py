from app import app
from flask import request, jsonify
from flask_json import as_json

from app.models.user import User
from app.models.review import Review
from app.models.review_user import ReviewUser
from app.models.review_place import ReviewPlace
from app.models.place import Place

app.config['JSON_ADD_STATUS'] = False

@app.route('/users/<int:user_id>/reviews', methods=['GET'])
def get_reviews(user_id):
	user_check = User.select().where(User.id == user_id)
	if not user_check.exists():
		return jsonify({"code": 404, "msg":"User does not exist"}), 404
	data = []
	query = Review.select().join(ReviewUser).where(ReviewUser.user_id == user_id)
	for row in query:
		data.append(row.to_hash())
	return jsonify(data)

@app.route('/users/<int:user_id>/reviews', methods=['POST'])
@as_json
def post_review(user_id):
    post_data = request.values
    if 'message' not in post_data and 'from_user_id' not in post_data:
    	return {"code": 400, "msg":"bad request, incomplete parameters"}, 400
    try:
    	user_query = User.get(User.id == int(post_data['from_user_id']))
    except:
    	return {"code": 404, "msg":"User does not exist or bad value of from_user_id"}, 404

    try:
    	user_to_query = User.get(User.id == user_id)
    except:
    	return {"code": 404, "msg":"from_user does not exist"}, 404
    new_review = Review.create(
    	message = post_data['message'],
    	user = user_query,
    )
    if 'stars' in post_data:
    	new_review.stars = int(post_data['stars'])
    	new_review.save()
    new_reviewUser = ReviewUser.create(
    	user = user_to_query,
    	review = new_review,
    )
    return new_review.to_hash()

@app.route('/users/<int:user_id>/reviews/<int:review_id>', methods=['GET'])
@as_json
def get_review(user_id, review_id):
	try:
		rev_query = Review.select().join(ReviewUser).where(ReviewUser.user_id == user_id, Review.id == review_id).get()
	except:
		return {"code": 404, "msg":"There are no reviews for this user"}, 404
	return rev_query.to_hash()

@app.route('/users/<int:user_id>/reviews/<int:review_id>', methods=['DELETE'])
@as_json
def delete_review(user_id, review_id):
	try:
		rev_query2 = ReviewUser.select().where(ReviewUser.user_id == user_id, ReviewUser.review_id == review_id).get()
		rev_query = Review.select().join(ReviewUser).where(ReviewUser.user_id == user_id, Review.id == review_id).get()
	except:
		return {"code": 404, "msg":"User does not exist"}, 404
	out_dict = rev_query.to_hash()
	rev_query2.delete_instance()
	return out_dict

@app.route('/places/<int:place_id>/reviews', methods=['GET'])
def get_reviews_by_place(place_id):
	reviews = []
	check_place = Place.select().where(Place.id == place_id)
	if not check_place.exists():
		return jsonify({"code": 404, "msg":"User does not exist"}), 404
	qq = Review.select().join(ReviewPlace).where(ReviewPlace.place == place_id)
	#if not qq.exists():
	#	return {"code": 404, "msg":"User does not exist"}, 404
	for row in qq:
		reviews.append(row.to_hash())
	return jsonify(reviews)


	# reviewplace_query = ReviewPlace.select().where(ReviewPlace.place == place_id)
	# #except:
	# #	return jsonify(reviews)
	# for row in reviewplace_query:
	# 	review_query = Review.get(Review.id == row.review)
	# 	reviews.append(review_query.to_hash())
	# return jsonify(reviews)

@app.route('/places/<int:place_id>/reviews', methods=['POST'])
@as_json
def post_review_by_place(place_id):
	post_data = request.values
	if 'message' not in post_data and 'from_user_id' not in post_data:
		return {"code": 400, "msg":"bad request, incomplete parameters"}, 400
	try:
		place_get = Place.get(Place.id == place_id)
	except:
		return {'code': 10004, 'msg': 'Place does not exist'}, 404
	try:
		user_get = User.get(User.id == int(post_data['from_user_id']))
	except:
		return {'code': 10004, 'msg': 'User does not exist'}, 400
	new_review = Review.create(
    	message = post_data['message'],
    	user = user_get,
    )
	if 'stars' in post_data:
		new_review.stars = int(post_data['stars'])
    	new_review.save()
	new_review_place = ReviewPlace.create(place=place_get, review=new_review)
	#new_review_user = ReviewUser.create(user=user_get, review=new_review)
	return new_review.to_hash()

@app.route('/places/<int:place_id>/reviews/<int:review_id>', methods=['GET'])
@as_json
def get_all_reviews_by_place(place_id, review_id):
	try:
		review_query = Review.select().join(ReviewPlace).where(ReviewPlace.place == place_id, Review.id == review_id).get()
	except:
		return {'code': 10004, 'msg': 'Place does not exist'}, 400
	return review_query.to_hash()

@app.route('/places/<int:place_id>/reviews/<int:review_id>', methods=['DELETE'])
@as_json
def delete_all_reviews_by_place(place_id, review_id):
	try:
		query = ReviewPlace.select().where(ReviewPlace.place == place_id).get()
		review_query = Review.select().join(ReviewPlace).where(ReviewPlace.place == place_id, Review.id == review_id).get()
	except:
		return {'code': 404, 'msg': 'User does not exist'}, 404
    
	out_dict = review_query.to_hash()
	query.delete_instance()
	review_query.delete_instance()
	return out_dict
