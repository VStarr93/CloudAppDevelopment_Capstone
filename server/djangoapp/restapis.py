import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator 
from ibm_watson.natural_language_understanding_v1 \
    import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
        # Call get method of requests library with URL and parameters
    response = requests.get(
        url, 
        params=kwargs,
        headers={'Content-Type': 'application/json'}
    )
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    print(json_data)
    return json_data
    # If any error occurs
    #print("Network exception occurred")

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    response = requests.post(url, params=kwargs, json=json_payload)
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
# - Call get_request() with specified arguments
    json_result = get_request(url)
# - Parse JSON results into a CarDealer object list
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result['detList']
        # For each dealer object
        for dealer in dealers: 
            # Get its content in 'doc' object
            #dealer_doc = dealer['doc']
            # Create a CarDealer object with values in 'doc' object
            dealer_obj = CarDealer(
                address=dealer['address'], 
                city=dealer['city'],
                full_name=dealer['full_name'],
                id=dealer['id'],
                lat=dealer['lat'],
                long=dealer['long'],
                short_name=dealer['short_name'],
                st=dealer['st'],
                state=dealer['state'],
                zip=dealer['zip'],
            )
            results.append(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    dealerId=kwargs.get('dealerId')
    if dealerId:
        # Call get_request() with specified parameters
        json_result = get_request(url, dealerId=dealerId)
    else:
        json_result = get_request(url)
        
    # Parse JSON results into a DealerReview object List
    if json_result:
        # Get the row list in JSON as reviews
        reviews = json_result['Reviews']
        # for each review object
        for review in reviews:
            # Create a DealerReview object with values in reviews object
            review_obj = DealerReview(
                dealership=review['dealership'],
                name=review['name'],
                purchase=review['purchase'],
                review=review['review'],
                purchase_date=review['purchase_date'],
                car_make=review['car_make'],
                car_model=review['car_model'],
                car_year=review['car_year'],
                id=review['_id'],
                sentiment=''
            )
            dealerreview = review_obj.review
            sentiment=analyze_review_sentiments(dealerreview)
            print(sentiment)
            review_obj.sentiment=sentiment
            results.append(review_obj)
    return results

# Create a get_dealer_by_id
def get_dealer_by_id(url, id, **kwargs):
    results = []
# - Call get_request() with specified arguments
    json_result = get_request(url, id=id)
# - Parse JSON results into a CarDealer object list
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result['detList']
        # For each dealer object
        for dealer in dealers: 
            # Create a CarDealer object with values in dealers object
            dealer_obj = CarDealer(
                address=dealer['address'], 
                city=dealer['city'],
                full_name=dealer['full_name'],
                id=dealer['id'],
                lat=dealer['lat'],
                long=dealer['long'],
                short_name=dealer['short_name'],
                st=dealer['st'],
                state=dealer['state'],
                zip=dealer['zip'],
            )
            results.append(dealer_obj)
    return dealer_obj

# Create a get_dealer_by_state
def get_dealer_by_state(url, st, **kwargs):
    results = []
# - Call get_request() with specified arguments
    json_result = get_request(url, st=st)
# - Parse JSON results into a CarDealer object list
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result['detList']
        # For each dealer object
        for dealer in dealers: 
            # Create a CarDealer object with values in dealers object
            dealer_obj = CarDealer(
                address=dealer['address'], 
                city=dealer['city'],
                full_name=dealer['full_name'],
                id=dealer['id'],
                lat=dealer['lat'],
                long=dealer['long'],
                short_name=dealer['short_name'],
                st=dealer['st'],
                state=dealer['state'],
                zip=dealer['zip'],
            )
            results.append(dealer_obj)
    return results

# Def analyze_review_sentiments(text):
def analyze_review_sentiments(text):
    # url = ''
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/37605604-7150-4aa2-a90f-64bb55e09f99"
    # api_key = '
    api_key = "H3SiImAh9Uj71OIjET2b2mnsc-Di9RRmVKCclhYmYKIR"
    # authenticator = IAMAuthenticator(api_key)
    authenticator = IAMAuthenticator(api_key)
    # natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01', authenticator=authenticator)
    nlu = NaturalLanguageUnderstandingV1(version='2022-04-07', authenticator=authenticator)
    # natural_language_understanding.set_service_url(url)
    nlu.set_service_url(url)
    # response = natural_language_understanding.analyze(text=text, features=Features(sentiment-SentimentOptions(targets=[text]))).get_result()
    response = nlu.analyze(
        text=text,
        features=Features(sentiment=SentimentOptions(targets=[text])),
        language="en"
    ).get_result()
    # label = json.dumps(response, indent=2)
    # label = response['sentiment']['document']['label']
    label = response['sentiment']['document']['label']
    # return(label)
    return label

# Create a get_all_reviews method
def get_all_reviews(url, **kwargs):
    results = []
    print("inside get_all_reviews")
    # Call get_request() with specified parameters
    json_result = get_request(url)
    # Parse JSON results into a DealerReview object List
    if json_result:
        # Get the row list in JSON as reviews
        reviews = json_result['Reviews']
        print("json_result returned - GetAllReviews")
        # for each review object
        for review in reviews:
            print("inside for statement")
            # Create a DealerReview object with values in reviews object
            review_obj = DealerReview(
                dealership=review['dealership'],
                name=review['name'],
                purchase=review['purchase'],
                review=review['review'],
                purchase_date=review['purchase_date'],
                car_make=review['car_make'],
                car_model=review['car_model'],
                car_year=review['car_year'],
                id=review['id'],
                sentiment=''
            )
            dealerreview = review_obj.review
            sentiment=analyze_review_sentiments(dealerreview)
            print(sentiment)
            review_obj.sentiment=sentiment
            results.append(review_obj)
        else:
            print("json_result did not return - GetAllReviews")
    return results
