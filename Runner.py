from Classes.TXT_extractor import TXTExtractor
from Classes.CSV_extractor import CSVExtractor
from Classes.s3_manager import S3Manager
from Classes.JSON_extractor import JSONExtractor


bucket_name = "data-eng-401-final-project"
s3 = S3Manager(bucket_name)
files_to_process = s3.list_files("Talent/")
for filename in files_to_process:
    file = s3.read_file_to_memory(filename)
    if filename.endswith(".csv"):
        file = CSVExtractor().extract(file)
        print(file)
    elif filename.endswith(".txt"):
        file = TXTExtractor().extract(file)
        print(file)
        print("newFile")
    elif filename.endswith(".json"):
        file = JSONExtractor().extract(file)




