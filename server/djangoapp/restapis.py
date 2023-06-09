import requests
import json
import sys, os
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from pprint import pprint
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

# this function is used to make get requests
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# This function is used make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    print(f"In post_request - POST to {url}")
    try:
        print("post_request - json_payload is: ", json_payload)
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        print("ERROR occurred while making POST request. ")
    status_code = response.status_code
    print("With status {} ".format(status_code))

    return response

"""
# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    print(json_result)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["entries"]
        # For each dealer object
        for dealer_doc in dealers:
            # Get its content in `doc` object
            #dealer_doc = dealers["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results
"""

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)

    if json_result:
        # Get the row list in JSON as dealers
        """
        dealers = json_result["rows"]
        """
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
"""
class DealerReview:

    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year,sentiment, id):
        self.dealership=dealership
        self.name=name
        self.purchase=purchase
        self.review=review
        self.purchase_date=purchase_date
        self.car_make=car_make
        self.car_model=car_model
        self.car_year=car_year
        self.sentiment=sentiment #from Watson NLU - will be positive, neutral, or negative.
        self.id=id

    def __str__(self):
        return "Review: " + self.review +\
                " Sentiment: " + self.sentiment
"""
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealer_id)
    #print("after json_result\n")
    #abc =  json_result
    #print("abc type is ",type(abc))
    #print(json_result)
    #reviewsObject = json.loads(json_result)
    #print("reviewObject = ", reviewsObject)
    #defg = json_result["data"]["docs"][0]
    #print("defg = ", defg)
    # dsg  if "entries" in json_result:
    if "data" in json_result:
        
        reviews = json_result["data"]["docs"]
        print("reviews = ", reviews)
        # For each review object
        for review in reviews:
            print("in reviews loop")
            review_obj = DealerReview(
                dealership=review["dealership"],
                name=review["name"],
                purchase=review["purchase"],
                review=review["review"],
                purchase_date=review["purchase_date"],
                car_make=review["car_make"],
                car_model=review["car_model"],
                car_year=review["car_year"],
                sentiment=analyze_review_sentiments(review["review"]),
                id=review['id']
                )
            print("review object = ", review_obj)
            results.append(review_obj)
            pprint(results)

    print("about to return results from get_dealer_reviews_from_cf\n")
    return results

# returns the deaker object with full information on a particular dealer
# as idientified by numeric dealer_id value
def get_dealer_by_id(url, dealer_id):
    # Call get_request with the dealer_id param
    json_result = get_request(url, dealerId=dealer_id)

    # Create a CarDealer object from response
    #dealer = json_result["entries"][0]
    dealer = json_result[0]
    # I only have "st" in my car dealer model, I may also need "state"
    dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                           id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                           short_name=dealer["short_name"],
                           #st=dealer["st"], state=dealer["state"], zip=dealer["zip"])
                           st=dealer["st"], zip=dealer["zip"])

    return dealer_obj

# returns the name oa a dealer based on the numeric id of thee dealer
# Requires the dealer_id parameter with only a single value
def get_dealer_name_by_id_from_cf(url, dealerId):
    # Call get_request with the dealer_id param
    json_result = get_request(url, dealerId=dealerId)

    # Create a CarDealer object from response
    dealer = json_result[0]["full_name"]
    print("in get_dealer_name_by_id_from_cf, full_name = ", dealer)
    """
    print("in get_dealer_name_by_id_from_cf: dealer = " , dealer)
    dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                          id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                           short_name=dealer["short_name"],
                           st=dealer["st"], state=dealer["state"], zip=dealer["zip"])

    return dealer_obj
    """
    return dealer




# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(review_text):
    # Watson NLU configuration
    """  this stuff is for real instalation
    try:
        if os.environ['env_type'] == 'PRODUCTION':
            url = os.environ['WATSON_NLU_URL']
            api_key = os.environ["WATSON_NLU_API_KEY"]
    except KeyError:
        url = config('WATSON_NLU_URL')
        api_key = config('WATSON_NLU_API_KEY')
    """
    #using os.envirol for local usage
    api_key = os.environ['NLUKEY']
    url = os.environ['NLU_URL']

    version = '2021-08-01'
    authenticator = IAMAuthenticator(api_key)
    nlu = NaturalLanguageUnderstandingV1(
        version=version, authenticator=authenticator)
    nlu.set_service_url(url)

    # tyis is where we get the sentiment of the review from NLU
    try:
        response = nlu.analyze(text=review_text, features=Features(
            sentiment=SentimentOptions())).get_result()
        print(json.dumps(response))

        sentiment_label = response["sentiment"]["document"]["label"]
    except:
        print("text is too short for meaningful analysis, so we will sentiment value to 'neutral' ")
        sentiment_label = "neutral"


    print(sentiment_label) # debug

    return sentiment_label

"""
def analyze_review_sentiments(dealerreview, **kwargs):

    #API_KEY="<NLU key goes here>"
    # actually using the key from IBM NLU
   NLUKEY = os.environ['NLUKEY']
    NLU_URL='https://api.us- south.natural-language-understanding.watson.cloud.ibm.com/instances/5a357be0-0b26-42cb-94f2-6024286a5e18'
    params = json.dumps({"text": dealerreview, "features": {"sentiment": {}}})
    response = requests.post(NLU_URL,data=params,headers={'Content-Type':'application/json'},auth=HTTPBasicAuth("apikey", NLUKEY))
    
    print(response.json())
    try:
        sentiment=response.json()['sentiment']['document']['label']
        return sentiment
    except:
        return "neutral"
"""