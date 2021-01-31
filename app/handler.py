import json
import logging
import base64
import sys
import numpy as np
import os, math, io, sys
from boto3 import Session
from PIL import Image
import requests 

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
    ouput_image = Mosaic(Image.open(filename), (128,128), None)
    output_image.render().save(filename)

    output = {}

    with open(filename, 'rb') as f:
        encoded_string = base64.b64encode(f.read()).decode("utf-8")
        output["picture"] = json.dumps(encoded_string)

    return output


class Mosaic():

    target_images = []
    mosaic_pieces = []

    def __init__(self, target_image, grid_size, input_images = None):
        
        #function splits the target image into a grid
        self._split_image(target_image, grid_size)
        self.avgs = []

        output_images = []
    
        if input_images is None:
            self._get_images()

        dims = (int(target_image.size[0] / grid_size[1]), int(target_image.size[1] / grid_size[0]))

        for img in self.mosaic_pieces:
            try:
                img.thumbnail(dims)
                self.avgs.append(self._rgb_ave(img))
            except ValueError:
                continue

        for img in self.target_images:
            avg = self._rgb_ave(img)
            match_index = self._match_image(avg)
            output_images.append(self.mosaic_pieces[match_index])

        self.mosaic_image = self._create_image_grid(output_images, grid_size)


    def render(self):
        return self.mosaic_image

    def _split_image(self, image, size):
        """
        PURPOSE: Divdes the image into pieces on the specificed size
        INPUT:
        image - The image that needs to be split up
        size - Tuple - The width and height to split the image up into
        """

        #dimensions of the input image 
        target_w, target_h = image.size[0], image.size[1] 

        m, n = size 
        w, h = int(target_w / n), int(target_h / m)

        for j in range(m):
            for i in range(n):
                self.target_images.append(image.crop((i * w, j * h, (i + 1) * w, (j + 1) * h)))


    # Obtain images to build the photo mosaic from
    def _get_images(self):

        url = "https://api.unsplash.com/photos/random?count=10"
        payload={}
        headers = {
            'Accept-Version': 'v1',
            'Authorization': 'Client-ID ' + os.environ.get("IMAGE_API_TOKEN") 
        }

        response = requests.request("GET", url, headers=headers, data=payload).json()

        count = 0
        for img in response:

            im = requests.get(img["urls"]["raw"])

            file = open(f"test{str(count)}.jpg", "wb")
            file.write(im.content)
            file.close()
            
            self.mosaic_pieces.append(Image.open(f"test{str(count)}.jpg"))
            count += 1
        

    # Average RGB values into a tuple of R, G, B averages
    def _rgb_ave(self, image):
        img = np.array(image)
        w, h, d = img.shape
        test = img.reshape(w * h, d)
        return tuple(np.average(img.reshape(w * h, d), axis=0))


    # Matches each target avg with the closest avg from the image bank
    def _match_image(self,target_avg):
        index = 0
        min_index = 0
        min_dist = float("inf")
        
        for avg in self.avgs:
            dist = math.sqrt((target_avg[0] - avg[0])**2 + (target_avg[1] - avg[1])**2 + (target_avg[2] - avg[2])**2)
            if dist < min_dist:
                min_dist = dist
                min_index = index
            index += 1
        return min_index

    # Creates a grid to layout new images on
    def _create_image_grid(self,images, dimensions):
        m, n = dimensions
        width = max([img.size[0] for img in images])
        height = max([img.size[1] for img in images])
        grid_img = Image.new('RGB', (n * width, m * height))

        for index in range(len(images)):
            row = int(index / n)
            col = index - n * row
            grid_img.paste(images[index], (col * width, row * height))
        return (grid_img)

