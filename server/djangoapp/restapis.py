import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        # Create an if statement for auth - NLU Service
        if api_key:
            #Basic authentication GET
            response = requests.get(
                url, 
                params=kwargs, 
                headers={'Content-Type': 'application/json'},
                auth=HTTPBasicAuth('apikey', api_key)
            )
        else:
            # No Authentication GET
            response = requests.get(
                url, 
                headers={'Content-Type': 'application/json'}, 
                params=kwargs
            )
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


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
def get_dealer_reviews_from_cf(url, dealerId, **kwargs):
    results = []
    # Call get_request() with specified parameters
    json_result = get_request(url, dealerId=dealerId)
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
                id=review['id'],
            )
            review_obj.sentiment=analyze_review_sentiments(review_obj.review)

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
    return results

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

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerreview):
# - Get the returned sentiment label such as Positive or Negative
    # results = []
    # Create Parameters
    params = dict()
    params['text'] = kwargs['dealerreview']
    params['version'] = kwargs['version']
    params['features'] = kwargs['features']
    params['return_analyzed_text'] = kwargs['return_analyzed_text']
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/37605604-7150-4aa2-a90f-64bb55e09f99"
    api_key = "pWyOpBuGY16kWDCXIVm2kn_B_GI9E6yo5G8-QRnTebJS"
# - Call get_request() with specified arguments
    json_result = get_request(
        url,
        params=params,
        headers={'Content-Type': 'application/json'},
        auth=HTTPBasicAuth('apikey', api_key)
    )
    # retreive setiment from json_result
    sentiment = json_result['features']['sentiment']
    # Return sentiment
    return sentiment