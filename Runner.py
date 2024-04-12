from Classes.TXT_extractor import TXTExtractor
from Classes.CSV_extractor import CSVExtractor
from Classes.s3_manager import S3Manager
from Classes.JSON_extractor import JSONExtractor
from Classes.data_upload_to_mongo import MongoUploader
from Classes.ProcessedFiles import ProcessedFilesManager
from Classes.CandidateAnalytics import CandidateAnalytics
from mongo_atlas_connect import *




bucket_name = "data-eng-401-final-project"
s3 = S3Manager(bucket_name)
S3col= ["Talent/", "Academy/"]
processed_files_path = 'processed_files.txt'
processed_objects = 'processed_objects.txt'
loader = MongoUploader()
filehandler = ProcessedFilesManager(processed_files_path)
objectHandler = ProcessedFilesManager(processed_objects)

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

print("All files processed")
print("uploading to mongo complete")
'''
## get the collection to see whats already in side and not repeate candidate uploads
## List of objects that have been processed already
collection = db['Candidates']
documents = list(collection.find())
list_of_objects_processed =[]
for doc in documents:

    file_name = f"Candidates/{doc['name'].replace(' ', '_')}.json"
    list_of_objects_processed.append(file_name)
## do we want to drop the Accademy col and Talent col since we have the Candidates col? meaning we dont have to worry about duplicate objects?
## this also means the we dont re create the same object and no need to double check. just after all obj created drop. only new files are added in the database then
## we redrop the 2 collections after we fill candidates up more.


# db['academy'].drop()
# db['talent'].drop()

### once dropped. no need for lists of any sort. just create the objects

## Some sort of runner code for the creation of objects.
print("Objects created successfully")

print("uploading objects to s3")
## no need to worry about duplicates. just upload all files to s3 since files for same name will overwrite each other
# Get all documents from the collection
documents = list(collection.find())

# Loop through the documents and upload each to S3
for doc in documents:
    # Convert the document to a JSON string
    doc_json = dumps(doc)

    # Use the '_id' field as the name for the JSON file
    file_name = file_name = f"Candidates/{doc['name'].replace(' ', '_')}_{doc['_id']}.json"

    # Upload to S3
    s3.s3.put_object(Body=doc_json, Bucket=bucket_name, Key=file_name)
    print(f"Uploaded {file_name} to S3 bucket {bucket_name}")


'''

analytics = CandidateAnalytics()


Declined_offers = analytics.candidates_declined_offer()

business012019 = analytics.applications_by_program_and_month("Business", 2019, 1)
Data012019 = analytics.applications_by_program_and_month("Data", 2019, 1)
Eng02019 = analytics.applications_by_program_and_month("Engineering", 2019, 1)

business022019 = analytics.applications_by_program_and_month("Business", 2019, 2)
Data022019 = analytics.applications_by_program_and_month("Data", 2019, 2)
Eng002019 = analytics.applications_by_program_and_month("Engineering", 2019, 2)

business032019 = analytics.applications_by_program_and_month("Business", 2019, 3)
Data032019 = analytics.applications_by_program_and_month("Data", 2019, 3)
Eng032019 = analytics.applications_by_program_and_month("Engineering", 2019, 3)

business042019 = analytics.applications_by_program_and_month("Business", 2019, 4)
Data042019 = analytics.applications_by_program_and_month("Data", 2019, 4)
Eng042019 = analytics.applications_by_program_and_month("Engineering", 2019, 4)

business052019 = analytics.applications_by_program_and_month("Business", 2019, 5)
Data052019 = analytics.applications_by_program_and_month("Data", 2019, 5)
Eng052019 = analytics.applications_by_program_and_month("Engineering", 2019, 5)

business062019 = analytics.applications_by_program_and_month("Business", 2019, 6)
Data062019 = analytics.applications_by_program_and_month("Data", 2019, 6)
Eng062019 = analytics.applications_by_program_and_month("Engineering", 2019, 6)

business072019 = analytics.applications_by_program_and_month("Business", 2019, 7)
Data072019 = analytics.applications_by_program_and_month("Data", 2019, 7)
Eng072019 = analytics.applications_by_program_and_month("Engineering", 2019, 7)

business082019 = analytics.applications_by_program_and_month("Business", 2019, 8)
Data082019 = analytics.applications_by_program_and_month("Data", 2019, 8)
Eng082019 = analytics.applications_by_program_and_month("Engineering", 2019, 8)



Overall_Academy_attendies = analytics.total_academy_attendees()

overall_Academy_passes = analytics.total_academy_passes()

total_academy_failures = analytics.total_academy_failures()

percentage_passed = analytics.percentage_passed() ## could just be a count of all passes and then divide by total number of passes

pass_rates_by_program = analytics.pass_rates_by_program()

top_inviters_for_passed_candidates = analytics.top_inviters_for_passed_candidates()
print("done with analytics")


