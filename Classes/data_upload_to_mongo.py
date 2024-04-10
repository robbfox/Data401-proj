from mongo_atlas_connect import *
import json
import pandas as pd

class MongoUploader():

    def format_identifier(self, data_input, collection):
        file_type = type(data_input)


        if collection == "Academy/":
            self.academy_dataframe_uploader(data_input)

        elif collection == "Talent/":
            if file_type == str:
                print("In JSON")
                self.json_uploader(data_input)
            else:
                print("In dataframe")
                self.talent_dataframe_uploader(data_input)

    def json_uploader(self, data_input):
        print("In JSON uploader")
        if isinstance(data_input, str):
            # If the input data is a string, attempt to parse it as JSON
            try:
                parsed_data = json.loads(data_input)
            except json.JSONDecodeError as e:
                print(f"Error parsing input data as JSON: {e}")
                return
        else:
            parsed_data = data_input

        # Check if parsed_data is a dictionary or a list of dictionaries
        if isinstance(parsed_data, dict):
            # If it's a single dictionary, insert it directly
            db.Talent.insert_one(parsed_data)
            print("Successfully uploaded in Talent")
        elif isinstance(parsed_data, list) and all(isinstance(item, dict) for item in parsed_data):
            # If it's a list of dictionaries, insert each dictionary separately
            db.Talent.insert_many(parsed_data)
            print("Successfully uploaded multiple documents in Talent")
        else:
            print("Error: input data is not a valid dictionary or a list of dictionaries")

    def talent_dataframe_uploader(self, data_input):
        # Check if data_input is a DataFrame with one or more rows
        if isinstance(data_input, pd.DataFrame):
            # Convert DataFrame to a list of dictionaries
            list_input_talent = data_input.to_dict(orient='records')
        elif isinstance(data_input, dict):
            # If it's a single dictionary, wrap it in a list
            list_input_talent = [data_input]
        else:
            raise ValueError("data_input must be a DataFrame or a dict")

        # Check if the list is not empty
        if list_input_talent:
            # Insert each dictionary from the list as a separate document into the Talent collection
            db.Talent.insert_many(list_input_talent)
            print(f"Successfully uploaded {len(list_input_talent)} records to Talent collection.")
        else:
            print("No records to upload to Talent collection.")

    def academy_dataframe_uploader(self, data_input):
        # Assuming data_input is a DataFrame with a single row
        if isinstance(data_input, pd.DataFrame):
            # Convert DataFrame to a single dict
            dict_input_academy = data_input.to_dict(orient='records')[0]
        else:
            raise ValueError("data_input must be a DataFrame with a single row")

        # Insert a single document into the Academy collection
        db.Academy.insert_one(dict_input_academy)
        print("Successfully uploaded in Academy")






