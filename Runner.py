from Classes.TXT_extractor import TXTExtractor
from Classes.CSV_extractor import CSVExtractor
from Classes.s3_manager import S3Manager
from Classes.JSON_extractor import JSONExtractor
from Classes.data_upload_to_mongo import MongoUploader
from Classes.ProcessedFiles import ProcessedFilesManager


bucket_name = "data-eng-401-final-project"
s3 = S3Manager(bucket_name)
S3col= ["Talent/", "Academy/"]
processed_files_path = 'processed_files.txt'
loader = MongoUploader()
filehandler = ProcessedFilesManager(processed_files_path)

processed_files_path = './processed_files.txt'
processed_files = filehandler.read_processed_files_list()
# files_to_process = s3.list_files("Talent/")

for col in S3col:
    files_to_process = s3.list_files(col)
    files_to_process = list(set(s3.list_files(col)))
    new_files = [f for f in files_to_process if f not in processed_files]

    print(len(new_files))

    for filename in new_files:
        file = s3.read_file_to_memory(filename)
        if filename.endswith(".csv"):
            file = CSVExtractor().extract(file,filename)
            print(filename)
            loader.format_identifier(file, col,filename)
        elif filename.endswith(".txt"):
            file = TXTExtractor().extract(file)
            print(filename)
            loader.format_identifier(file, col,filename)
        elif filename.endswith(".json"):
            file = JSONExtractor().extract(file)
            print(filename)
            loader.format_identifier(file, col,filename)
        filehandler.write_processed_file(filename)






