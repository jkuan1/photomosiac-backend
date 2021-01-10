import json
from .mosaic import photoMosaic
import logging

def handler(event, context):

    logging.error(event)

    mosaic = photoMosaic(event, (256,256))

    response = {
        "statusCode": 200,
        "picture": mosaic
    }

    return response
