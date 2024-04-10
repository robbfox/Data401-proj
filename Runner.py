from Classes.TXT_extractor import TXTExtractor
from Classes.CSV_extractor import CSVExtractor
from Classes.s3_manager import S3Manager
from Classes.JSON_extractor import JSONExtractor
from Classes.data_upload_to_mongo import MongoUploader


bucket_name = "data-eng-401-final-project"
s3 = S3Manager(bucket_name)
S3col= ["Talent/", "Academy/"]
loader = MongoUploader()

# files_to_process = s3.list_files("Talent/")

for col in S3col:
    files_to_process = s3.list_files(col)
    files_to_process = list(set(s3.list_files(col)))
    print(len(files_to_process))

    for filename in files_to_process:
        file = s3.read_file_to_memory(filename)
        if filename.endswith(".csv"):
            file = CSVExtractor().extract(file)
            print(file)
            loader.format_identifier(file, col)
        elif filename.endswith(".txt"):
            file = TXTExtractor().extract(file)
            print(file)
            loader.format_identifier(file, col)
        elif filename.endswith(".json"):
            pass
            #file = JSONExtractor().extract(file)
            #loader.format_identifier(file, col)






