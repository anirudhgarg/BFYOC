import logging
import json
import azure.functions as func


def main(req: func.HttpRequest, docList: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    ratingId = req.params.get('ratingId')
    if not docList:
        logging.warning('Document list not found.')
        return func.HttpResponse(
             "Please pass a valid rating Id on the query string or in the request body",
             status_code=400) 
    else:
        return func.HttpResponse(json.dumps(docList[0]['rating']), status_code=200)
    
