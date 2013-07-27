import json
import linecache
from pprint import pprint



## loads the review we want to predict. 
## n is the number from the top of the list of reviews.
## returns the business id and the user id of the review.
def load_review(directory, n):
	line = linecache.getline(directory, n)
	review = json.loads(line)
	return review["user_id"], review["business_id"]  

## gathers a business / user profile given the id, directory, and field ("business_id" or "user_id").
def find_id_data(id, field, directory):
	data = []

	with open(directory) as file:
		for line in file:
			parsed = json.loads(line)
			if parsed[field] == id:
				data.append(parsed)

	return data

def weighted_avr(reviews):
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
			rating, number = weighted_avr(reviews)
			avr_ratings.append(rating)
			n_of_ratings.append(number)
		else:
			avr_ratings.append(0)
			n_of_ratings.append(0)

	return avr_ratings, n_of_ratings
## MAIN ##

if __name__ == '__main__':

	## load the review we want to predict
	test_direc = "Data/yelp_test_set/yelp_test_set_review.json"
	user_id, biz_id = load_review(test_direc, 1)
	print "IDs: ", user_id, biz_id
	print

	## load the profile of the business
	biz_direc = "Data/yelp_test_set/yelp_test_set_business.json"
	biz = find_id_data(biz_id, "business_id", biz_direc)
	print biz
	print

	## load he profile of the user
	user_direc = "Data/yelp_test_set/yelp_test_set_user.json"
	user = find_id_data(user_id, "user_id", user_direc)
	print user
	print

	## find reviews of the restaurant and find average
	# review_direc = "Data/yelp_training_set/yelp_training_set_review.json"
	# reviews = find_id_data(biz_id, "business_id", review_direc)
	# if reviews:
	# 	rating, number = weighted_avr(reviews)
	# 	print "Rating: ", rating, "Number: ", number

	ratings, n_of_ratings = find_avr_rating([biz_id])
	print ratings, n_of_ratings



	# directory = "Data/yelp_training_set/yelp_training_set_business.json"
	# data = load_data(directory)
	# pprint(data)
