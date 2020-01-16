import logging
import json
import azure.functions as func


def main(req: func.HttpRequest, docList: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    responseJson = []
    if not docList:
        logging.warning('Document list not found.')
        return func.HttpResponse(
             "Please pass a valid user Id on the query string or in the request body",
             status_code=400) 
    else:
        for doc in docList:
            responseJson.append(doc.to_json())
        return func.HttpResponse(json.dumps(responseJson), status_code=200)
    
