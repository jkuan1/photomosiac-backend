import numpy as np
import os, math
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

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

def rgbAverage(image):
    img = np.array(image)
    w, h, d = img.shape
    test = img.reshape(w * h, d)
    return tuple(np.average(img.reshape(w * h, d), axis=0))

def splitImage(image, size):
    W, H = image.size[0], image.size[1] #Target image dimensions
    m, n = size #Split image size
    w, h = int(W / m), int(H / n)
    imgs = []
    for i in range(m):
        for j in range(n):
            imgs.append(image.crop((j * w, i * h, (j + 1) * w, (i + 1) * h)))
    return(imgs)

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

def photoMosaic(target_image, input_images, grid_size):
    target_images = splitImage(target_image, grid_size)
    output_images = []
    count = 0
    batch_size = 256
    avgs = []
    for img in input_images:
        try:
            avgs.append(rgbAverage(img))
        except ValueError:
            continue
    
    for img in target_images:
        avg = rgbAverage(img)
        match_index = matchImage(avg, avgs)
        output_images.append(input_images[match_index])
        if count > 0 and batch_size > 10 and count % batch_size is 0:
            print('processed %d of %d...' % (count, len(target_images)))
        count += 1

    mosaic_image = createImageGrid(output_images, grid_size)
    return (mosaic_image)

# test_image = Image.open("blep.jpg")
# test_avg = rgbAverage(test_image)
# match_image = Image.open("ESO_Centaurus_A_LABOCA.jpg")
# match_avg = rgbAverage(match_image)
# images=getImages("./input_images")

    