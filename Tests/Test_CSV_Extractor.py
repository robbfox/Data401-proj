import unittest
import boto3
import tempfile
import pandas as pd

from Classes.CSV_extractor import CSVExtractor

class TestCSVExtractor(unittest.TestCase):
    def setUp(self):
        # Fetch CSV data from S3 bucket
        boto3_client = boto3.client('s3')
        csv_object = boto3_client.get_object(Bucket='data-eng-401-final-project', Key='Academy/Business_20_2019-02-11.csv')
        csv_data = csv_object['Body'].read()
        self.csv_data = csv_data.decode('utf-8')

    def test_extraction(self):
        extractor = CSVExtractor()
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write(self.csv_data)
        with open(temp_file.name, 'rb') as file:
            file_contents = file.read()
        extracted_df = extractor.extract(file_contents, "")
        self.assertIsInstance(extracted_df, pd.DataFrame)  # Check if the result is a DataFrame
        self.assertEqual(extracted_df.shape[0], 8)  # Check if there are 8 rows
        self.assertEqual(extracted_df.shape[1], 50) # Check if there are 50 columns
        self.assertTrue((extracted_df == 0).any().any()) # Check if there are any zeros
        self.assertFalse((extracted_df == None).any().any()) # Ensure there are no None values
        self.assertFalse((extracted_df == '').any().any()) # Ensure there are no empty strings
        self.assertFalse((extracted_df == ' ').any().any()) # Ensure there are no spaces

        for index, row in extracted_df.iterrows():
            # Check if a zero value is present in the row
            if 0 in row.values:
                # Get the index of the first zero value
                zero_index = list(row.values).index(0)
                # Slice the row to get values to the right of the zero value
                values_to_right = row.iloc[zero_index + 1:]
                # Check if all values to the right are also zeros
                self.assertTrue((values_to_right == 0).all(),
                                f"Not all values to the right of zero in row {index} are zeros")

        temp_file.close()
