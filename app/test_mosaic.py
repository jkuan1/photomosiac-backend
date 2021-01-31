import unittest
from handler import Mosaic
from PIL import Image

class TestMosaic(unittest.TestCase):

    def test_Mosaic(self):

        target_image = Image.open("test_input.jpg")
        grid_size = (32,32)

        mosaic_file = Mosaic(target_image, grid_size).render()
        mosaic_file.save("test_result.jpg")

if __name__ == "__main__":
    unittest.main()