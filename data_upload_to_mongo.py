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
        #json_input_academy = data_input.to_json(orient='records')
        #dict_input_academy = json.loads(json_input_academy)
        dict_input_academy = data_input.to_json(orient='records')
        #dict_input_academy = data_input.to_dict(orient='records')
        print(type(dict_input_academy))
        if isinstance(dict_input_academy, dict):
            db.Academy.insert_one(dict_input_academy)
            print("successfully uploaded in Academy")
        else:
            print("Error: dict_input_academy is not a valid dictionary")
        #db.Academy.insert_one(dict_input_academy)
        #print("successfully uploaded in Academy")


mongo_input = MongoUploader()
data_input = pd.read_csv('Data_30_2019-04-08.csv')
print(data_input)
mongo_input.format_identifier(data_input)
#print(type(data_input))




