import numpy as np
import math
from PIL import Image

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
    
    avg=avgs
    for avg in avgs:
        dist = math.sqrt((target_avg[0] - avg[0])**2 + (target_avg[1] - avg[1])**2 + (target_avg[2] - avg[2])**2)

    return dist


test_image = Image.open("blep.jpg")
test_avg = rgbAverage(test_image)
match_image = Image.open("ESO_Centaurus_A_LABOCA.jpg")
match_avg = rgbAverage(match_image)
print(matchImage(test_avg, match_avg))
