#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
#import sys

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibmcloudant.cloudant_v1 import CloudantV1

def main(dict):
    # Create variables
    apikey = dict['__bx_creds']['cloudantnosqldb']['apikey']
    url = dict['__bx_creds']['cloudantnosqldb']['host']
    completeUrl = "https://" + url
    
    # Create the authenticator.
    authenticator = IAMAuthenticator(apikey)
    
    # Construct the service instance.
    cloudant = CloudantV1(authenticator=authenticator)
    cloudant.set_service_url(completeUrl)
    
    dealerId = 'dealerId'
    # if dealerId
    if dealerId in dict:
        # Query a list of filtered Documents    
        dealer = dict['dealerId']
        dealerId = int(dealer)
        # filteredDocs = cloudant.post_find(
        #     db = "reviews",
        #     selector = {'dealership':{'$eq': dealerId }}
        # ).get_result()['docs']
        # return {"Reviews": filteredDocs}
        filteredDocs = cloudant.post_view(
            db = "reviews",
            ddoc = "9bdf0054c820e33f17b7022dd78f2e25bf2c7d6e",
            view = "by-dealerid",
            key = dealerId
        ).get_result()['rows']
        return {"Reviews": filteredDocs}
    else:
        
        allReviews = cloudant.post_view(
            db = "reviews",
            ddoc = "9bdf0054c820e33f17b7022dd78f2e25bf2c7d6e",
            view = "by-dealerid",
        ).get_result()["rows"]
        return {"Reviews": allReviews}