import json
import logging
import base64
import sys
import numpy as np
import os, math, io, sys
from boto3 import Session
from PIL import Image

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):

    # Retrieves image from API request
    body = base64.b64decode(event["body"].split(",",2)[-1])

    #temporarily saves the input picture in tmp directory (on lambda) or in current folder as a jpg
    try:
        filename = '/tmp/tmp.jpg' 
        with open(filename, 'wb') as f:
            f.write(body)
    except:
        filename = "tmp.jpg"
        with open(filename, 'wb') as f:
            f.write(body)
    
    #create the mosaic 
    mosaic = mosaic_generator(Image.open(filename), (128,128), None)
    mosaic.save(filename)

    output = {}

    with open(filename, 'rb') as f:
        encoded_string = base64.b64encode(f.read()).decode("utf-8")
        output["picture"] = json.dumps(encoded_string)

    return output

# Create a mosaic_generator of the target image using a bank of images
def mosaic_generator(target_image, grid_size, input_images=None):
    target_images = splitImage(target_image, grid_size)
    output_images = []
    count = 0
    batch_size = int(len(target_images) / 10)
    avgs = []

    if input_images is None:
        input_images = boto3Images()
        pass

    dims = (int(target_image.size[0] / grid_size[1]), int(target_image.size[1] / grid_size[0]))

    for img in input_images:
        try:
            
            img.thumbnail(dims)
            avgs.append(rgbAverage(img))
        except ValueError:
            continue

    for img in target_images:
        avg = rgbAverage(img)
        match_index = matchImage(avg, avgs)
        output_images.append(input_images[match_index])
        if count > 0 and batch_size > 10 and count % batch_size == 0:
            print('Processed %d of %d...' % (count, len(target_images)))
        count += 1

    mosaic_image = createImageGrid(output_images, grid_size)
    return (mosaic_image)

def boto3Images():
    ACCESS_KEY = os.environ.get("aws_id")
    SECRET_KEY = os.environ.get("aws_secret")
    images = []

    session = Session(aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    s3 = session.resource('s3')
    bucket = s3.Bucket('photos-nwhacks-2021')

    for s3_file in bucket.objects.all():
        object = bucket.Object(s3_file.key)
        file_stream = io.BytesIO()
        object.download_fileobj(file_stream)
        img = Image.open(file_stream)
        images.append(img)

    return(images)


Image.MAX_IMAGE_PIXELS = None

# Obtain images from a directory to build the photo mosaic from
def getImages(directory):
    files = os.listdir(directory) 
    images = []
    for file in files:
        filePath = os.path.abspath(os.path.join(directory, file))
        
        try:
            fp = open(filePath, "rb")
            im = Image.open(fp)
            images.append(im)
            im.load()
            fp.close()
        except:
            print("Invalid image: %s" % (filePath,))
    return (images)

# Average RGB values into a tuple of R, G, B averages
def rgbAverage(image):
    img = np.array(image)
    w, h, d = img.shape
    test = img.reshape(w * h, d)
    return tuple(np.average(img.reshape(w * h, d), axis=0))

# Divdes the image into pieces on the specificed size
def splitImage(image, size):
    W, H = image.size[0], image.size[1] #Target image dimensions
    m, n = size #Split image size
    w, h = int(W / n), int(H / m)
    imgs = []
    for j in range(m):
        for i in range(n):
            imgs.append(image.crop((i * w, j * h, (i + 1) * w, (j + 1) * h)))
    return(imgs)

# Matches each target avg with the closest avg from the image bank
def matchImage(target_avg, avgs):
    index = 0
    min_index = 0
    min_dist = float("inf")
    
    for avg in avgs:
        dist = math.sqrt((target_avg[0] - avg[0])**2 + (target_avg[1] - avg[1])**2 + (target_avg[2] - avg[2])**2)
        if dist < min_dist:
            min_dist = dist
            min_index = index
        index += 1
    return (min_index)

# Creates a grid to layout new images on
def createImageGrid(images, dimensions):
    m, n = dimensions
    width = max([img.size[0] for img in images])
    height = max([img.size[1] for img in images])
    grid_img = Image.new('RGB', (n * width, m * height))

    for index in range(len(images)):
        row = int(index / n)
        col = index - n * row
        grid_img.paste(images[index], (col * width, row * height))
    return (grid_img)

