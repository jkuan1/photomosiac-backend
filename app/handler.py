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
    try:
        filename = '/tmp/tmp.jpg' 
        with open(filename, 'wb') as f:
            f.write(body)
    except:
        filename = "tmp.jpg"
        with open(filename, 'wb') as f:
            f.write(body)

    with open(filename, 'wb') as f:
        f.write(body)
        
    mosaic = photoMosaic(Image.open(filename), (128,128), None)

    logger.info("FINISHED")

    mosaic.save(filename)

    encoded_string = ""

    with open(filename, 'rb') as f:
        encoded_string = base64.b64encode(f.read()).decode("utf-8")

    logger.info("RETURN")

    return { "picture": json.dumps(encoded_string) }

        

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
