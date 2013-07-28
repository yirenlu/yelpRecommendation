import json
import linecache
from pprint import pprint
import numpy
import math


## loads the review we want to predict. 
## n is the number from the top of the list of reviews.
## returns the business id and the user id of the review.

def load_review(directory, n):
	line = linecache.getline(directory, n)
	review = json.loads(line)
	return review["user_id"], review["business_id"]

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

## MAIN ##

if __name__ == '__main__':

	## load the review we want to predict
	test_direc = "Data/yelp_test_set/yelp_test_set_review.json"
	user_id, biz_id = load_review(test_direc, 1)
	#print "IDs: ", user_id, biz_id
	#print

	## load the profile of the business
	biz_direc = "Data/yelp_test_set/yelp_test_set_business.json"
	biz = find_id_data(biz_id, "business_id", biz_direc)
	#print biz
	#print

	## load he profile of the user
	user_direc = "Data/yelp_test_set/yelp_test_set_user.json"
	user = find_id_data(user_id, "user_id", user_direc)
	#print user

	## find reviews of the restaurant and find average
	#ratings, n_of_ratings = find_avr_rating([biz_id])
	#print ratings, n_of_ratings

	## load a training review
	training_direc = "Data/yelp_training_set/yelp_training_set_review.json"
	user1, biz1 = load_review(training_direc, 3)
	user2, biz2 = load_review(training_direc, 8)
	#print biz1, biz2

	computes_business_similarity(biz1, biz2)
		
	# directory = "Data/yelp_training_set/yelp_training_set_business.json"
	# data = load_data(directory)
	# pprint(data)


	## testing if I can commit.
