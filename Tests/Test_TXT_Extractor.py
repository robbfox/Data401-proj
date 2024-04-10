import unittest
from unittest.mock import MagicMock, patch
from Classes.TXT_extractor import TXTExtractor
import io
class TestTXTExtractor(unittest.TestCase):
    def test_extract_from_local_file(self):
        extractor = TXTExtractor()

        # Define test data for a local file
        test_data = (
            "Wednesday 18 September 2019\n"
            "London Academy\n"
            "\n"
            "JAQUENETTA CATONNE -  Psychometrics: 60/100, Presentation: 28/32\n"
            "CELLO RICIOPPO -  Psychometrics: 55/100, Presentation: 20/32\n"
            "BERRI COCKLIN -  Psychometrics: 63/100, Presentation: 17/32\n"
        )



        # Mock the open function to return the test data
        with patch("builtins.open", unittest.mock.mock_open(read_data=test_data)):
            # Call the extract method with a dummy file path
            result = extractor.extract("Talent/Sparta Day 11 December 2019.txt")

            # Assertions to validate the extraction
            self.assertIsInstance(result, str)  # Check if the result is a string
            self.assertTrue(result.startswith('['))  # Check if the result starts with a '[' indicating JSON array
            self.assertTrue(result.endswith(']'))  # Check if the result ends with a ']' indicating JSON array

    def test_extract_from_s3(self):
        extractor = TXTExtractor()

        s3_client_mock = MagicMock()

        # Define test data for S3 response
        test_data = (
            "Wednesday 18 September 2019\n"
            "London Academy\n"
            "\n"
            "JAQUENETTA CATONNE -  Psychometrics: 60/100, Presentation: 28/32\n"
            "CELLO RICIOPPO -  Psychometrics: 55/100, Presentation: 20/32\n"
            "BERRI COCKLIN -  Psychometrics: 63/100, Presentation: 17/32\n"
        )

        s3_client_mock.get_object.return_value = {
            'Body': MagicMock(return_value=test_data.encode())
        }

        # Set the S3 client for the extractor
        extractor.s3_client = s3_client_mock

        # Call the extract method with an empty file path (mocked for S3)
        result = extractor.extract("/Talent/Sparta Day 11 December 2019.txt")

        # Assertions to validate the extraction
        self.assertIsInstance(result, str)  # Check if the result is a string
        self.assertTrue(result.startswith('['))  # Check if the result starts with a '[' indicating JSON array
        self.assertTrue(result.endswith(']'))  # Check if the result ends with a ']' indicating JSON array

if __name__ == "__main__":
    unittest.main()
