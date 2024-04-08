
import unittest
from unittest.mock import MagicMock
from Classes.TXT_extractor import TXTExtractor
import pandas as pd

class TestTXTExtractor(unittest.TestCase):
    def test_extract_from_local_file(self):
        extractor = TXTExtractor()

        # Define test data for a local file
        test_data = (
            "2024-04-08\n"
            "Location: XYZ\n"
            "JAQUENETTA CATONNE -  Psychometrics: 60/100, Presentation: 28/32\n"
            "CELLO RICIOPPO -  Psychometrics: 55/100, Presentation: 20/32\n"
            "BERRI COCKLIN -  Psychometrics: 63/100, Presentation: 17/32\n"
        )

        # Mock the open function to return the test data
        with unittest.mock.patch("builtins.open", unittest.mock.mock_open(read_data=test_data)):
            # Call the extract method with a dummy file path
            df = extractor.extract("dummy_file.txt")

            # Assertions to validate the extraction
            self.assertIsInstance(df, pd.DataFrame)  # Check if the result is a DataFrame
            self.assertEqual(len(df), 3)  # Check if the DataFrame has 3 rows

    def test_extract_from_s3(self):
        extractor = TXTExtractor()

        s3_client_mock = MagicMock()

        # Define test data for S3 response
        test_data = (
            "2024-04-08\n"
            "Location: XYZ\n"
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
        df = extractor.extract("")

        # Assertions to validate the extraction
        self.assertIsInstance(df, pd.DataFrame)  # Check if the result is a DataFrame
        self.assertEqual(len(df), 3)  # Check if the DataFrame has 3 rows

if __name__ == "__main__":
    unittest.main()
