import json
from .mosaic import photoMosaic
import logging
import base64
import sys
from PIL import Image

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):

    # try:
    # print(f'event: {event}')
    body = base64.b64decode(event["body"].split(",",2)[-1])
    # print(f'{body}')
    
    # print(body)
    # img = base64.decodebytes(body)
    
    # print(img)
    
    # mosaic = photoMosaic(img, (256, 256))
    filename = '/tmp/tmp.jpg'  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
        f.write(body)
        
    mosaic = photoMosaic(Image.open(filename), (32,32), None)

    logger.info("FINISHED")

    
    return mosaic

    # except Exception as exp:
    #     print(exp)

        # exception_type, exception_value, exception_traceback = sys.exc_info()
        # traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)
        # err_msg = json.dumps({
        #     "errorType": exception_type.__name__,
        #     "errorMessage": str(exception_value),
        #     "stackTrace": traceback_string
        # })
        # logger.error(err_msg)
