import json

class JSONExtractor:
    def __init__(self):
        pass

    def extract(self, file):
        try:
            json_data = json.loads(file)
            return json_data
        except json.JSONDecodeError as e:
            raise ValueError("Failed to parse file content as JSON: {}".format(e))
