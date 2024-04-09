import unittest
from unittest.mock import patch, MagicMock
from Classes.s3_manager import S3Manager
import boto3


class TestS3Manager(unittest.TestCase):
    @patch('boto3.client')
    def setUp(self, mock_s3_client):
        self.s3_paginator_mock = MagicMock()
        self.s3_client_mock = MagicMock()
        self.s3_client_mock.get_paginator.return_value = self.s3_paginator_mock
        self.s3_paginator_mock.paginate.return_value = [
            {'Contents': [{'Key': 'Academy/test.csv'}, {'Key': 'Academy/test2.csv'}]},
            {'Contents': [{'Key': 'Talent/test.json'}, {'Key': 'Talent/test2.json'}]}
        ]

        self.s3_client_mock.get_object.return_value = {
            'Body': MagicMock(read=MagicMock(return_value=b"Name,Score\nJohn Doe,100"))
        }

        self.bucket_name = "data-eng-401-final-project"

    @patch('boto3.client', return_value=MagicMock())
    def test_list_files(self, mock_boto_client):
        mock_boto_client.return_value = self.s3_client_mock
        s3_manager = S3Manager(self.bucket_name)

        # Testing Academy files
        academy_files = s3_manager.list_files("Academy/")
        self.assertEqual(len(academy_files), 4)
        self.assertIn("Academy/test.csv", academy_files)

        # Testing Talent files
        talent_files = s3_manager.list_files("Talent/")
        self.assertEqual(len(talent_files), 4)
        self.assertIn("Talent/test.json", talent_files)

    @patch('boto3.client', return_value=MagicMock())
    def test_read_file_to_memory(self, mock_boto_client):
        mock_boto_client.return_value = self.s3_client_mock
        s3_manager = S3Manager(self.bucket_name)

        # Testing reading file to memory
        content = s3_manager.read_file_to_memory("Academy/test.csv")
        self.assertIsNotNone(content)
        self.assertEqual(content, b"Name,Score\nJohn Doe,100")
if __name__ == "__main__":
    unittest.main()
