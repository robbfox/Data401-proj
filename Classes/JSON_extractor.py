import json


class JSONExtractor:
    def __init__(self):
        pass

    def extract(self, file):
        # Check if the file is empty
        if file.strip() == "{}":
            raise ValueError("The JSON file is empty.")

        try:
            json_data = json.loads(file)
            return json_data
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse file content as JSON: {e}")
