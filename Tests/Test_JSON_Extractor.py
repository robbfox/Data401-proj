import unittest
from Classes.JSON_extractor import JSONExtractor


class TestJSONExtractor(unittest.TestCase):
    def test_extract(self):
        # Content of the provided JSON file
        file = ('{"name": "Stillmann Castano", "date": "22/08/2019", "tech_self_score": {"C#": 6, "Java": 5, '
                '"R": 2, "JavaScript": 2}, "strengths": ["Charisma"], "weaknesses": ["Distracted", '
                '"Impulsive", "Introverted"], "self_development": "Yes", "geo_flex": "Yes", '
                '"financial_support_self": "Yes", "result": "Pass", "course_interest": "Business"}')

        # Initialize JSONExtractor
        json_extractor = JSONExtractor()

        # Extract JSON data
        extracted_json = json_extractor.extract(file)

        # Define the expected JSON data
        expected_json = {
            "name": "Stillmann Castano",
            "date": "22/08/2019",
            "tech_self_score": {"C#": 6, "Java": 5, "R": 2, "JavaScript": 2},
            "strengths": ["Charisma"],
            "weaknesses": ["Distracted", "Impulsive", "Introverted"],
            "self_development": "Yes",
            "geo_flex": "Yes",
            "financial_support_self": "Yes",
            "result": "Pass",
            "course_interest": "Business"
        }

        # Check if the extracted JSON matches the expected JSON
        self.assertEqual(extracted_json, expected_json)


if __name__ == "__main__":
    unittest.main()
