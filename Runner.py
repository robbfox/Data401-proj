from bson.json_util import dumps
from Classes.TXT_extractor import TXTExtractor
from Classes.CSV_extractor import CSVExtractor
from Classes.s3_manager import S3Manager
from Classes.JSON_extractor import JSONExtractor
from Classes.data_upload_to_mongo import MongoUploader
from Classes.ProcessedFiles import ProcessedFilesManager
from Classes.CandidateAnalytics import CandidateAnalytics
from mongo_atlas_connect import *
from Classes.mongo_model import *


inserter = CreateCandidate()
bucket_name = "data-eng-401-final-project"
s3 = S3Manager(bucket_name)
S3col= ["Talent/", "Academy/"]
processed_files_path = 'processed_files.txt'
#processed_objects = 'processed_objects.txt'   ## may not need this
loader = MongoUploader()
filehandler = ProcessedFilesManager(processed_files_path)
#objectHandler = ProcessedFilesManager(processed_objects)

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
            #print(filename)
            loader.format_identifier(file, col,filename)
        elif filename.endswith(".txt"):
            file = TXTExtractor().extract(file)
            #print(filename)
            loader.format_identifier(file, col,filename)
        elif filename.endswith(".json"):
            file = JSONExtractor().extract(file)
            #print(filename)
            loader.format_identifier(file, col,filename)
        filehandler.write_processed_file(filename)

print("All files processed")
print("uploading raw files to mongo complete")
print("Process 30% complete")

collection = db['Candidates']
# documents = list(collection.find())
# list_of_objects_processed =[]
# for doc in documents:
#
#     file_name = f"Candidates/{doc['name'].replace(' ', '_')}.json"
#     list_of_objects_processed.append(file_name)


regex_pattern = re.compile(r".json$")
json_docs = db.Talent.find({"File origin": {"$regex": regex_pattern}},
                           {"name": 1, "date": 1, "_id": 0})

for json_doc in json_docs:
    input_name = json_doc['name']
    input_date = json_doc['date']
    inserter.get_id_talent(input_name, input_date)
    print(f"Inserted candidate for {input_name}")







db['Academy'].drop()
db['Talent'].drop()




print("Objects created successfully and inserted into Candidates collection")
print("Process 70% complete")
print("uploading objects to s3")

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



print("All objects uploaded to s3")
print("Process 100% complete")
print("Starting analytics")


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

#print all the analytics
print("Declined offers: ", Declined_offers)
print("***********************************")
print("individual program applications by month:")
print("january 2019")
print("===================================")
print("Business 01/2019: ", business012019)
print("Data 01/2019: ", Data012019)
print("Engineering 01/2019: ", Eng02019)
print(" ")
print("February 2019")
print("===================================")
print("Business 02/2019: ", business022019)
print("Data 02/2019: ", Data022019)
print("Engineering 02/2019: ", Eng002019)
print(" ")
print("March 2019")
print("===================================")
print("Business 03/2019: ", business032019)
print("Data 03/2019: ", Data032019)
print("Engineering 03/2019: ", Eng032019)
print(" ")
print("April 2019")
print("===================================")
print("Business 04/2019: ", business042019)
print("Data 04/2019: ", Data042019)
print("Engineering 04/2019: ", Eng042019)
print(" ")
print("May 2019")
print("===================================")
print("Business 05/2019: ", business052019)
print("Data 05/2019: ", Data052019)
print("Engineering 05/2019: ", Eng052019)
print(" ")
print("June 2019")
print("===================================")
print("Business 06/2019: ", business062019)
print("Data 06/2019: ", Data062019)
print("Engineering 06/2019: ", Eng062019)
print(" ")
print("July 2019")
print("===================================")
print("Business 07/2019: ", business072019)
print("Data 07/2019: ", Data072019)
print("Engineering 07/2019: ", Eng072019)
print(" ")
print("Aug 2019")
print("===================================")
print("Business 08/2019: ", business082019)
print("Data 08/2019: ", Data082019)
print("Engineering 08/2019: ", Eng082019)
print("===================================")




print("Overall Academy Attendies: ", Overall_Academy_attendies)
print("Overall Academy Passes: ", overall_Academy_passes)
print("Total Academy Failures: ", total_academy_failures)
print("Percentage Passed: ", percentage_passed)
print("Pass Rates by Program: ", pass_rates_by_program)
print("Top Inviters for Passed Candidates: ", top_inviters_for_passed_candidates)

print("done with analytics")


