import unittest

from Classes.data_extractor import DataExtractor

class TestDataExtractor(unittest.TestCase):
    def test_abstract_method(self):
        with self.assertRaises(NotImplementedError):
            DataExtractor().extract("path/to/file")