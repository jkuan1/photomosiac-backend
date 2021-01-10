import unittest
from ...app import mosaic


class TestMosaic(unittest.TestCase):

    def test_rbg_ave(self):

        image = "placeholder"
        ans = "placeholder"

        ave = mosaic.rgbAverage(image)
        self.assertEqual(ave, ans)

        return

if __name__ == "__main__":
    unittest.main()