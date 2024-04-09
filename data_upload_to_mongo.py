from mongo_atlas_connect import *
import json
import pandas as pd

class MongoUploader():
    def format_identifier(self, data_input):
        file_type = type(data_input)
        print(file_type)
        if file_type == str:
            print("In JSON")
            self.json_uploader(data_input)
        else:
            print("In dataframe")
            self.dataframe_uploader(data_input)

    def json_uploader(self, data_input):
        print("In JSON uploader")
        with open(data_input, 'r') as file:
            file_content = file.read()
        dict_input_talent = json.loads(file_content)
        print(dict_input_talent)
        db.Talent.insert_one(dict_input_talent)
        print("successfully uploaded in Talent")

    def dataframe_uploader(self, data_input):
        list_input_academy = data_input.to_dict(orient='records')
        print(type(list_input_academy))
        if isinstance(list_input_academy,list):
            for record in list_input_academy:
                db.Academy.insert_one({"data": record})
            print("successfully uploaded in Academy")
        else:
            print("Error: dict_input_academy is not a valid dictionary")








