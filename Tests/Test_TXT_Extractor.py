import unittest
from unittest.mock import MagicMock, patch
from Classes.TXT_extractor import TXTExtractor
import io

import json


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
        ## string to bytes

        test_data=test_data.encode('utf-8')  ## OBJECT OF BYTES
        result = extractor.extract(test_data)


        self.assertIsInstance(result, str)  # Check if the result is a string
        self.assertTrue(result.startswith('['))  # Check if the result starts with a '[' indicating JSON array
        self.assertTrue(result.endswith(']'))  # Check if the result ends with a ']' indicating JSON array

    def test_json_output(self):
        extractor = TXTExtractor()
          # Check if the json_output is a list

    # Define test data for a local file
        test_data = (
            "Wednesday 18 September 2019\n"
            "London Academy\n"
            "\n"
            "JAQUENETTA CATONNE -  Psychometrics: 60/100, Presentation: 28/32\n"
            "CELLO RICIOPPO -  Psychometrics: 55/100, Presentation: 20/32\n"
            "BERRI COCKLIN -  Psychometrics: 63/100, Presentation: 17/32\n"
        )
        test_data=test_data.encode('utf-8')  ## OBJECT OF BYTES
        result = extractor.extract(test_data)
        result_json = json.loads(result)
        self.assertIsInstance(result_json, list)

    def test_returns_date_in_correct_format(self):
        extractor = TXTExtractor()
        # Define test data for a local file
        test_data = (
            "Wednesday 8 September 2019\n"
            "London Academy\n"
            "\n"
            "JAQUENETTA CATONNE -  Psychometrics: 60/100, Presentation: 28/32\n"
            "CELLO RICIOPPO -  Psychometrics: 55/100, Presentation: 20/32\n"
            "BERRI COCKLIN -  Psychometrics: 63/100, Presentation: 17/32\n"
        )
        test_data=test_data.encode('utf-8')  ## OBJECT OF BYTES
        result = extractor.extract(test_data)
        result_json = json.loads(result)
        print(result_json, '>>>')

        self.assertEqual(result_json[0]["date"], "08/09/2019")
        self.assertEqual(result_json[1]["date"], "08/09/2019")
        self.assertEqual(result_json[2]["date"], "08/09/2019")


    # Convert the result to a JSON object








if __name__ == "__main__":
    unittest.main()