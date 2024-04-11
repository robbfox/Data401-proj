from mongo_atlas_connect import *
import re
class CreateCandidate:
    def get_id_talent(self, name, date):
        regex_pattern = re.compile(r".json$")
        file_origin = db.Talent.find_one({"name": name, "date": date, "File origin": {"$regex": regex_pattern}},
         {"File origin": 1, "_id": 0})
        print(file_origin)
        #file_origin_dict = dict(file_origin)
        print(type(file_origin))
        file_name = file_origin["File origin"]
        print(file_name)
        candidate_id = file_name.split('/')[1].split('.')[0]
        print(candidate_id)



name_id = CreateCandidate()
name_id.get_id_talent('Edvard Northen', '07/08/2019')