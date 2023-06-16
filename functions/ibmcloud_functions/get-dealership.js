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
 const couchurl = "https://" + url;
 cloudant.setServiceUrl(couchurl);
   
 try {
     if(params.st) {
         paramsSt = params.st ;
         
         const allDocs = await cloudant.postView({
             db: "dealerships",
             ddoc: "5432c5692bba7aaa7136a1e9a27a53902d3e442f",
             view: "by-state",
             key: paramsSt ,
         });
         const detList = allDocs.result.rows ;
         return { detList };
         
     } else if(params.id) {
         paramsId = parseInt(params.id);
         
         const allDocs = await cloudant.postView({
             db: "dealerships",
             ddoc: "5432c5692bba7aaa7136a1e9a27a53902d3e442f",
             view: "by-id",
             key: paramsId ,
         });
         const detList = allDocs.result.rows ;
         return { detList };
         
     } else {
         const allDocs = await cloudant.postView({
             db: "dealerships",
             ddoc: "5432c5692bba7aaa7136a1e9a27a53902d3e442f",
             view: "by-id",
         });
         const detList = allDocs.result.rows
         return { detList };
     };
     
 } catch (error) {
       return { error: error.description };
 };
}
