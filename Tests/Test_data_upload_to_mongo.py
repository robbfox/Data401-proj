import unittest
from unittest.mock import MagicMock
from Classes.data_upload_to_mongo import MongoUploader


class TestMongoUploader(unittest.TestCase):

    def setUp(self):
        self.uploader = MongoUploader()
        self.uploader.academy_dataframe_uploader = MagicMock()
        self.uploader.talent_dataframe_uploader = MagicMock()
        self.uploader.json_uploader = MagicMock()

    def test_format_identifier_academy(self):
        # Test for Academy data
        test_data = MagicMock()
        self.uploader.format_identifier(test_data, "Academy/", "test_file.csv")
        self.uploader.academy_dataframe_uploader.assert_called_with(test_data, "test_file.csv")

    def test_format_identifier_talent_dataframe(self):
        # Test for Talent data with DataFrame input
        test_data = MagicMock()
        self.uploader.format_identifier(test_data, "Talent/", "test_file.csv")
        self.uploader.talent_dataframe_uploader.assert_called_with(test_data, "test_file.csv")

    def test_format_identifier_talent_json(self):
        # Test for Talent data with JSON string input
        test_data = ('{"name": "Sydel Fenne", "date": "28/08/2019", "tech_self_score": {"Java": 3, "SPSS": 4}, '
                     '"strengths": ["Passionate"], "weaknesses": ["Perfectionist", "Sensitive"], "self_development": '
                     '"Yes", "geo_flex": "Yes", "financial_support_self": "Yes", "result": "Pass", "course_interest": '
                     '"Data"}')
        self.uploader.format_identifier(test_data, "Talent/", "test_file.json")
        self.uploader.json_uploader.assert_called_with(test_data, "test_file.json")


if __name__ == '__main__':
    unittest.main()
