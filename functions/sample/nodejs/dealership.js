/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
 const { CloudantV1 } = require('@ibm-cloud/cloudant');
 const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
     const authenticator = new IamAuthenticator({ apikey: params.__bx_creds.cloudantnosqldb.apikey });
     const cloudant = CloudantV1.newInstance({
         authenticator: authenticator
     });
     const url = params.__bx_creds.cloudantnosqldb.host;
     const couchurl = "https://" + url ;
     cloudant.setServiceUrl(couchurl);
     
     try {
       let dbList = await cloudant.getAllDbs();
       let allDocs = await cloudant.postAllDocs({
           db: params.dbname ,
           includeDocs: true ,
       });
       let state = "CA" ;
       let stateLength = state.length ;
       
       if(state.length == 2) {
           const _selectorDocs = await cloudant.postFind({
               db: "dealerships" ,
               selector: {"state": state} ,
           });
       } else {
           let _selectorDocs = await cloudant.postFind({
               db: "dealerships" ,
               selector: {"state": "Texas"} ,
           });
       };
       
       
       let detList = [];
       let docs = selectorDocs.result.docs;
       docs.forEach(element => {
           let details = {
               "id": element.id,
               "city": element.city,
               "state": element.state,
               "st": element.st,
               "address": element.address,
               "zip": element.zip,
               "lat": element.lat,
               "long": element.long,
           };
           detList.push(details);
       });
       return { detList };
     } catch (error) {
         return { error: error.description };
     }
}

