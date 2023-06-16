#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibmcloudant.cloudant_v1 import CloudantV1, Document

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
    
    # Put Document
    new_review = cloudant.put_document(
        db= "reviews",
        doc_id= str(dict['review']['id']),
        document= dict['review']
    ).get_result()
    
    return {"Reviews": new_review }
    
