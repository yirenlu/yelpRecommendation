import json
import linecache
from pprint import pprint
import numpy
import math

## Directories!

biz_test_direc = "Data/yelp_test_set/yelp_test_set_business.json"
biz_train_direc = "Data/yelp_training_set/yelp_training_set_business.json"

user_test_direc = "Data/yelp_test_set/yelp_test_set_user.json"
user_train_direc = "Data/yelp_training_set/yelp_training_set_user.json"

rev_test_direc = "Data/yelp_test_set/yelp_test_set_review.json"
rev_training_direc = "Data/yelp_training_set/yelp_training_set_review.json"

## loads the review we want to predict. 
## n is the number from the top of the list of reviews.
## returns the user id and the business id of the review.

def load_review(directory, n):
	line = linecache.getline(directory, n)
	review = json.loads(line)
	if 'stars' in review:
		return review["user_id"], review["business_id"], review["stars"]
	else:
		return review["user_id"], review["business_id"], None

## retrieves the review that user_id gave business_id
def get_review_entry(user_id, business_id, directory):
	with open(directory) as file:
		for line in file:
			parsed = json.loads(line)
			if parsed['user_id'] == user_id and parsed['business_id'] == business_id:
				return parsed['stars']

## gathers a business / user profile given the id, directory, and field ("business_id" or "user_id").
def find_id_data(id, field, directory):
	data = []

	with open(directory) as file:
		for line in file:
			parsed = json.loads(line)
			if parsed[field] == id:
				data.append(parsed)

	return data

def avr(reviews):
	n = len(reviews)
	stars = 0
	for review in reviews:
		stars += review["stars"]

	return float(stars)/float(n), n 

def find_avr_rating(business_id_list):
	review_direc = "Data/yelp_training_set/yelp_training_set_review.json"

	avr_ratings = []
	n_of_ratings = []

	for business_id in business_id_list:
		reviews = find_id_data(biz_id, "business_id", review_direc)
		if reviews:
			rating, number = avr(reviews)
			avr_ratings.append(rating)
			n_of_ratings.append(number)
		else:
			avr_ratings.append(0)
			n_of_ratings.append(0)

	return avr_ratings, n_of_ratings

def cosine_distance(u, v):
    """
    Returns the cosine of the angle between vectors v and u. This is equal to
    u.v / |u||v|.
    """
    #print u,v
    return numpy.dot(u, v) / (math.sqrt(numpy.dot(u, u)) * math.sqrt(numpy.dot(v, v)))

def computes_business_similarity(business_id_1, business_id_2):
	'''computes the similarity between two given businesses according to cosine similarity'''

	review_direc = "Data/yelp_training_set/yelp_training_set_review.json"
	business_1_vector = []
	business_2_vector = []

	### calculated by observing users who have rated both items
	reviews_of_business_1 = find_id_data(business_id_1, "business_id", review_direc)
	reviews_of_business_2 = find_id_data(business_id_2, "business_id", review_direc)
	co_raters = [review['user_id'] for review in reviews_of_business_1 for review2 in reviews_of_business_2 if review['user_id'] == review2['user_id']]
	
	for rater in co_raters:
		rating1 = [review['stars'] for review in reviews_of_business_1 if review['user_id'] == rater]
		rating2 = [review['stars'] for review in reviews_of_business_2 if review['user_id'] == rater]
		business_1_vector.append(rating1.pop(0))
		business_2_vector.append(rating2.pop(0))

	# uses either cosine or correlation similarity metric
	similarity = cosine_distance(business_1_vector, business_2_vector)
	print 'The similarity of these two items is %s' % similarity

## calculates the average
def avr_error_user_mean():
	for n in range(1, 5000):
		user_id, biz_id, stars = load_review(rev_training_direc, n)

		user = find_id_data(user_id, "user_id", user_train_direc)
		user_avr_rating = user['average_stars']

		biz = find_id_data(biz_id, "business_id", biz_train_direc)
		biz_avr_rating = biz['stars']

		# find whatever metric we are interested in.
		
## MAIN ##

if __name__ == '__main__':


	for n in range(1, 1000):
	## load the review we want to predict
		
		user_id, biz_id, _ = load_review(rev_test_direc, n)
		print "IDs: ", user_id, biz_id

		biz = find_id_data(user_id, "user_id", user_test_direc)
		if biz:
			print "test"
		biz = find_id_data(user_id, "user_id", user_train_direc)	
		if biz:
			print "train"
			
		print

	## load the profile of the business
	
	
	#print

	## load the profile of the user
	# user_direc = "Data/yelp_test_set/yelp_test_set_user.json"
	# user = find_id_data(user_id, "user_id", user_direc)
	#print user

	## find reviews of the restaurant and find average
	# ratings, n_of_ratings = find_avr_rating([biz_id])
	# print ratings, n_of_ratings

	# training_direc = "Data/yelp_training_set/yelp_training_set_review.json"
	# user_reviews = find_id_data(user_id, 'user_id', training_direc)
	# print user_reviews
	# businesses = [review["business_id"] for review in user_reviews]
	# ratings_list, n_of_ratings_list = find_avr_rating(businesses)

	# print ratings_list
	# print n_of_ratings_list




	## ----- Ren's stuff ------

	## load a training review
	# training_direc = "Data/yelp_training_set/yelp_training_set_review.json"
	# user1, biz1 = load_review(training_direc, 3)
	# user2, biz2 = load_review(training_direc, 8)
	# #print biz1, biz2

	# computes_business_similarity(biz1, biz2)
		
	# directory = "Data/yelp_training_set/yelp_training_set_business.json"
	# data = load_data(directory)
	# pprint(data)


	## testing if I can commit.
