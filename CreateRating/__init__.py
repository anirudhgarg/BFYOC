import logging
import requests
import uuid
import datetime
import json

import azure.functions as func

def main(req: func.HttpRequest, doc: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    prod_id = req_body['productId']
    productId = requests.get(f'https://serverlessohproduct.trafficmanager.net/api/GetProduct?productId={prod_id}')
    if productId.status_code != 200:
        return func.HttpResponse(
             'Invalid productId',
             status_code=400
        )

    user_id = req_body['userId']
    userID = requests.get(f'https://serverlessohuser.trafficmanager.net/api/GetUser?userId={user_id}')
    if userID.status_code != 200:
        return func.HttpResponse(
             'Invalid userId',
             status_code=400
        )

    uniqueId = str(uuid.uuid4())
    timestamp = str(datetime.datetime.utcnow())
    rating = req_body['rating']
    if (not is_int(rating)) or (int(rating) < 0 or int(rating) > 5):
        return func.HttpResponse(
             'rating value is invalid',
             status_code=400
        )

    rating_data = {
        'id' : uniqueId,
        'userId': req_body['userId'],
        'productId': req_body['productId'],
        'timestamp': timestamp,
        'locationName': req_body['locationName'],
        'rating': int(req_body['rating']),
        'userNotes': req_body['userNotes']
    }

    doc.set(func.Document.from_json(json.dumps(rating_data)))
    return func.HttpResponse(
        json.dumps(rating_data),
        mimetype='application/json',
    )

def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
