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
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
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
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



