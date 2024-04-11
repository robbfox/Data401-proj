from Classes.TXT_extractor import TXTExtractor
from Classes.CSV_extractor import CSVExtractor
# from Classes.s3_manager import S3Manager
from Classes.JSON_extractor import JSONExtractor
from Classes.data_upload_to_mongo import MongoUploader
from Classes.mongo_model import *

bucket_name = "data-eng-401-final-project"
# s3 = S3Manager(bucket_name)
S3col = ["Talent/", "Academy/"]

# loader = MongoUploader()
inserter = CreateCandidate()
# files_to_process = s3.list_files("Talent/")
#
# for col in S3col:
#     files_to_process = s3.list_files(col)
#     files_to_process = list(set(s3.list_files(col)))
#
#     print(len(files_to_process))
#
#     for filename in files_to_process:
#         file = s3.read_file_to_memory(filename)
#         if filename.endswith(".csv"):
#             file = CSVExtractor().extract(file,filename)
#             print(filename)
#             loader.format_identifier(file, col,filename)
#         elif filename.endswith(".txt"):
#             file = TXTExtractor().extract(file)
#             print(filename)
#             loader.format_identifier(file, col,filename)
#         elif filename.endswith(".json"):
#             file = JSONExtractor().extract(file)
#             print(filename)
#             loader.format_identifier(file, col,filename)

regex_pattern = re.compile(r".json$")
json_docs = db.Talent.find({"File origin": {"$regex": regex_pattern}},
                                  {"name": 1, "date": 1, "_id": 0})

for json_doc in json_docs:
    input_name = json_doc['name']
    input_date = json_doc['date']
    inserter.get_id_talent(input_name, input_date)
print("Inserted Successfully")





