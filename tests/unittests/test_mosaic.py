import unittest
from ...app.handler import Mosaic


class TestMosaic(unittest.TestCase):

    def test_Mosaic(self):

        

        mosaic_file = Mosaic(target_image, grid_size).render()
        mosaic_file.save("./test_image")
        mosaic_file.show()

if __name__ == "__main__":
    unittest.main()