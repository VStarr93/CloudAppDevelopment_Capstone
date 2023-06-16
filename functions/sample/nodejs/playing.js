const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');
const params = {
    "__bx_creds": {
        "cloudantnosqldb": {
            "host": "b88ab149-fb9a-42a4-aba0-cf76674cb93e-bluemix.cloudantnosqldb.appdomain.cloud" ;
            "apikey": "7WFu-ei8anC_Mm5Jv1BRWw-3BaXp2sI8geTEg77dJfwk" ;
            "username": "b88ab149-fb9a-42a4-aba0-cf76674cb93e-bluemix" ;
        };
    };
    "state": "California" ;
};


async function main(params) {
    const authenticator = new IamAuthenticator({ apikey: params.__bx_creds.cloudantnosqldb.apikey });
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    const url = params.__bx_creds.cloudantnosqldb.host;
    const couchurl = "https://" + url;
    cloudant.setServiceUrl(couchurl);
      
    try {
        const state = params.state ;
        const stateLength = state.length ;
        
        if(stateLength>2) {
            const state1 = "state" ,
        } else {
            const state1 = "st" ,
        };
        
        const selectorDocs = await cloudant.postFind({
            db: "dealerships" ,
            selector: {state1: {"$eq": state}} ,
        });
        
        const detList = [];
        const docs = selectorDocs.result.docs;
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
