import json
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

    def test_extract_date(self):
        file = {"name": "Michel Lebarree",
                "date": "07/08/2019",
                "tech_self_score": {"Python": 3, "Java": 4, "Ruby": 1, "R": 2, "PHP": 2, "C++": 3},
                "strengths": ["Versatile"],
                "weaknesses": ["Controlling", "Perfectionist", "Chatty"],
                "self_development": "Yes",
                "geo_flex": "Yes",
                "financial_support_self": "Yes",
                "result": "Pass",
                "course_interest": "Engineering"}

        file_json = json.dumps(file)
        json_extractor = JSONExtractor()
        extracted_date = json_extractor.extract(file_json)["date"]
        expected_date = "07/08/2019"

        self.assertEqual(extracted_date, expected_date)

    def test_extract_empty_json(self):
        # Test with empty JSON content
        file = '{}'
        json_extractor = JSONExtractor()
        expected_json = {}
        extracted_json = json_extractor.extract(file)
        self.assertEqual(extracted_json, expected_json)

    def test_extract_list(self):
        file = {"name": "Orly Lorens",
                "date": "01/08/2019",
                "tech_self_score": {"Ruby": 2, "R": 5, "SPSS": 1, "JavaScript": 1},
                "strengths": ["Ambitious", "Independent", "Passionate"],
                "weaknesses": ["Conventional", "Passive"],
                "self_development": "No",
                "geo_flex": "Yes",
                "financial_support_self": "Yes",
                "result": "Fail",
                "course_interest": "Business"}

        file_json = json.dumps(file)
        json_extractor = JSONExtractor()
        extracted_list = type(json_extractor.extract(file_json)["strengths"])
        expected_list = type(["Ambitious", "Independent", "Passionate"])

        self.assertEqual(extracted_list, expected_list)

    def test_extract_dict(self):
        file = {"name": "Cooper Ingraham",
                "date": "14/08/2019",
                "tech_self_score": {"C#": 3, "Java": 1, "PHP": 4},
                "strengths": ["Versatile", "Rational"],
                "weaknesses": ["Immature"],
                "self_development": "Yes",
                "geo_flex": "Yes",
                "financial_support_self": "No",
                "result": "Fail",
                "course_interest": "Business"}

        file_json = json.dumps(file)
        json_extractor = JSONExtractor()
        extracted_dict = type(json_extractor.extract(file_json)["tech_self_score"])
        expected_dict = type({"C#": 3, "Java": 1, "PHP": 4})

        self.assertEqual(extracted_dict, expected_dict)

    def test_extract_name(self):
        file = {"name": "Hannah Messum",
                "date": "29/08/2019",
                "tech_self_score": {"Python": 8, "Ruby": 2, "JavaScript": 2},
                "strengths": ["Reliable", "Passionate"],
                "weaknesses": ["Intolerant"],
                "self_development": "Yes",
                "geo_flex": "Yes",
                "financial_support_self": "Yes",
                "result": "Fail",
                "course_interest": "Data"}

        file_json = json.dumps(file)
        json_extractor = JSONExtractor()
        extracted_name = json_extractor.extract(file_json)["name"]
        expected_name = "Hannah Messum"

        self.assertEqual(extracted_name, expected_name)


if __name__ == "__main__":
    unittest.main()
