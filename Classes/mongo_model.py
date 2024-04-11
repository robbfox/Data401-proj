from mongo_atlas_connect import *
import re
class CreateCandidate:


    def get_id_talent(self, input_name, input_date):
        regex_pattern = re.compile(r".json$")
        file_origin = db.Talent.find_one({"name": input_name, "date": input_date, "File origin": {"$regex": regex_pattern}},
         {"File origin": 1, "_id": 0})
        file_name = file_origin["File origin"]
        candidate_id = file_name.split('/')[1].split('.')[0]
        self.insert_candidate_id(candidate_id, input_name)
        self.retrieve_candidate_info(candidate_id, input_name)

    def insert_candidate_id(self, candidate_id, input_name):
        db.Talent.update_many(
            {"name": input_name},
            {"$set": {"candidate_id": candidate_id}})
        db.Academy.update_many(
            {"name": input_name},
            {"$set": {"candidate_id": candidate_id}})

    def retrieve_candidate_info(self, candidate_id, input_name):
        regex_pattern_json = re.compile(r".json$")
        details_json = db.Talent.find_one(
            {"candidate_id": candidate_id, "File origin":{"$regex": regex_pattern_json}},
            {})
        regex_pattern_csv = re.compile(r".csv$")
        personal_info_csv = db.Talent.find_one(
            {"candidate_id": candidate_id, "File origin": {"$regex": regex_pattern_csv}},
            {})
        regex_pattern_txt = re.compile(r".txt$")
        sparta_day_txt = db.Talent.find_one(
            {"candidate_id": candidate_id, "File origin": {"$regex": regex_pattern_txt}},
            {})
        regex_pattern_csv_2 = re.compile(r".csv$")
        academy_scores_csv = db.Academy.find_one(
            {"candidate_id": candidate_id, "File origin": {"$regex": regex_pattern_csv_2}},
            {})

        self.final_insert_into_candidates(details_json, personal_info_csv,
                               sparta_day_txt, academy_scores_csv, input_name, candidate_id)

    def final_insert_into_candidates(self, details_json, personal_info_csv,
                               sparta_day_txt, academy_scores_csv, input_name, candidate_id):

        data = {
            "_id": candidate_id,
            "name": input_name,
            "sparta_day_results": sparta_day_txt,
            "interview_overview": details_json,
            "academy_scores": academy_scores_csv,
            "personal_info": personal_info_csv
        }

        result = db.Candidates.find_one({"_id": candidate_id}, {})
        if result is None:
            db.Candidates.insert_one(data)


# name_id = CreateCandidate()
# name_id.get_id_talent('Edvard Northen', '07/08/2019')
# name_id.get_id_talent('Hilary Willmore', '01/08/2019')
#