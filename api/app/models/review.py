from peewee import *
import base
from user import User

'''defines review for user and place'''
class Review(base.BaseModel):
	message = TextField(null=False)
	stars = IntegerField(default=0)
	user = ForeignKeyField(related_name="reviews", rel_model=User, on_delete='CASCADE')

	'''returns row of review as a dict'''
	def to_dict(self):
		from review_place import ReviewPlace
		from review_user import ReviewUser
		
		review_dict = super(Review, self).to_dict()
		if 'reviewuser' in dir(self):
			print "ggg"
		try:
			reviewplace_query = ReviewPlace.get(ReviewPlace.review == self.id)
			reviewplace = reviewplace_query.place_id
		except:
			reviewplace = None
		
		try:
			reviewuser_query = ReviewUser.get(ReviewUser.review == self.id)
			reviewuser = reviewuser_query.user_id
		except:
			reviewuser = None

		review_dict.update({
			"message": self.message,
			"stars": self.stars,
			"from_user_id": self.user.id,
			"to_user_id":  reviewuser,
			"to_place_id": reviewplace,
		})
		return review_dict