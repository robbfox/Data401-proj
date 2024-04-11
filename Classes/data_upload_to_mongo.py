from mongo_atlas_connect import *
import json
import pandas as pd

class MongoUploader():

    def format_identifier(self, data_input, collection, file_origin):
        # Determine the type of data input
        file_type = type(data_input)

        if collection == "Academy/":
            # For Academy data
            self.academy_dataframe_uploader(data_input, file_origin)
        elif collection == "Talent/":
            # For Talent data
            if file_type == str:
                # If data_input is a string (JSON)
                self.json_uploader(data_input, file_origin)
            else:
                # If data_input is a DataFrame
                self.talent_dataframe_uploader(data_input, file_origin)

    def json_uploader(self, data_input, file_origin):
        # Parse the JSON data
        parsed_data = json.loads(data_input) if isinstance(data_input, str) else data_input

        # Insert 'File origin' into each document
        if isinstance(parsed_data, dict):
            parsed_data["File origin"] = file_origin
            db.Talent.insert_one(parsed_data)
        elif isinstance(parsed_data, list):
            for document in parsed_data:
                document["File origin"] = file_origin
            db.Talent.insert_many(parsed_data)

        print(f"Successfully uploaded JSON data from {file_origin}")

    def talent_dataframe_uploader(self, data_input, file_origin):
        # Convert the DataFrame to a list of dictionaries and add 'File origin'
        documents = data_input.to_dict(orient='records') if isinstance(data_input, pd.DataFrame) else [data_input]

        for document in documents:
            document["File origin"] = file_origin

        # Insert documents into the collection
        db.Talent.insert_many(documents)
        print(f"Successfully uploaded DataFrame data from {file_origin} to Talent collection.")

    def academy_dataframe_uploader(self, data_input, file_origin):
        # Handle academy data similarly to talent data
        documents = data_input.to_dict(orient='records') if isinstance(data_input, pd.DataFrame) else [data_input]

        for document in documents:
            document["File origin"] = file_origin

        db.Academy.insert_many(documents)
        print(f"Successfully uploaded DataFrame data from {file_origin} to Academy collection.")





