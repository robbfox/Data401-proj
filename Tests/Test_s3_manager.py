import unittest
from unittest.mock import patch, MagicMock
from moto import mock_aws
from Classes.s3_manager import S3Manager
import boto3


class TestS3Manager(unittest.TestCase):
    @patch('boto3.client')
    def setUp(self, mock_s3_client):
        # Configure the mock to simulate the S3 client behavior
        self.mock_s3_client = mock_s3_client

        # Mock the response of 'list_objects_v2' and 'get_object'
        self.mock_s3_client.return_value.list_objects_v2.return_value = {
            'Contents': [{'Key': 'Academy/test.csv'}, {'Key': 'Talent/test.json'}]
        }
        self.mock_s3_client.return_value.get_object.return_value = {
            'Body': MagicMock(read=MagicMock(return_value=b"Name,Score\nJohn Doe,100"))
        }

        self.bucket_name = "data-eng-401-final-project"
        self.s3_manager = S3Manager(self.bucket_name)

    def test_list_files(self):
        academy_files = self.s3_manager.list_files("Academy/")
        self.assertEqual(len(academy_files), 2)
        self.assertIn("Academy/test.csv", academy_files)

        talent_files = self.s3_manager.list_files("Talent/")
        self.assertEqual(len(talent_files), 2)
        self.assertIn("Talent/test.json", talent_files)

    def test_read_file_to_memory(self):
        content = self.s3_manager.read_file_to_memory("Academy/test.csv")
        self.assertIsNotNone(content)
        self.assertEqual(content, b"Name,Score\nJohn Doe,100")

if __name__ == "__main__":
    unittest.main()
