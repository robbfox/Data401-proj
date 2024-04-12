# Data401 final project
This project runs an Extract-Transform-Load data pipeline, built in Python. The data consists of various types of information files that are stored in an AWS S3 bucket. The files are in .csv, JSON or .txt format, and contain info about potential and current students at the Sparta Academy. The code uses object-oriented programming, creating classes to inspect the files in S3, read to memory, clean and format the data as required, and load into MongoAtlas, a NoSQL database. 

## Team roles
Product Owner: Xuanyu Lin (Jack), Scrum Master: Lihong Zheng
The team decided to delegate tasks into two teams: an extract and transform team (Brian Luna, Muhammad Nuwaz, Robert Fox & Lihong Zheng) and an upload & query team (Rahul Batra, Shivani Batish, Shreya Jain & Usama Asghar).

## Data extraction
Our first step is to extract the data files from the Amazon S3 bucket and clean them. A number of extractors were built for this purpose (as described below). 

## Components:
1. CSV Extractor (csv_extractor.py)
This script extracts data from CSV files, performs data cleaning and manipulation tasks, and returns a Pandas DataFrame.

2. JSON Extractor (json_extractor.py)
The JSON extractor script extracts data from JSON files, handling empty files and JSON parsing errors.

3. Text File (TXT) Extractor (txt_extractor.py)
The TXT extractor script extracts structured data from text files, parses participant information, and outputs JSON data.

4. MongoDB Model (mongo_model.py)
This script defines a MongoDB model for managing candidate data. It includes methods for linking data from multiple collections and inserting data into the Candidates collection.

5. Processed Files Manager (processed_files.py)
The processed files manager script provides functionality to read and write lists of processed files to a specified file. It's useful for tracking which files have already been processed.

6. S3 Manager (s3_manager.py)
The S3 manager script manages interactions with AWS S3, including reading files from S3 buckets and uploading files to S3 buckets.

## Dependencies
* pandas
* pymongo
* boto3 (for interacting with AWS S3)

## Mongo Atlas Setup:
MongoDB Atlas, a cloud-based version of the NoSQL Database MongoDB was selected by the team with the vision to create a one-person view of the extracted and cleaned Sparta Global data.
 
The team created accounts on MongoDB Atlas, one of the team created a Database called “data-401-final-project” and invited the fellow team members to join the project as collaborators through adding their emails. Upon joining the project, the collaborators were required to add their IP address to make full use of the shared project.
 
## Collections
This database would be receiving data from the Talent and Academy categories. Talent refers to all of the data including personal information, competencies, and test scores etc on a person that is being considered to join Sparta up until they join if they pass and accept the offer. Academy data includes the weekly scores of each Sparta trainee out of 5 tested competencies. Therefore, in the database there are two Collections named “Talent” and “Academy” that will receive this data. A third collection named “Candidates” exists that pulls in the respective data from Talent and Academy for each unique person to create a one-person view comprising all of their information.

## Uploading the data into MongoDB
File: data_upload_to_mongo
Running the above file takes in the input (cleaned data) and inserts them into either the Talent or Academy Collection in the MongoDB database buy identifying the ending of the file e.g. .JSON.
 
## Linking together separate documents
This markdown describes how we identified overlapping data in each document from the Talent and Academy bucket to create reference points to build our one-person view (in the Candidate collection). The Applicant name and test date are the main linking attributes we have used.

### Talent Bucket
- **json - individual applicant details**
  - Key information in file:
    - Applicant name
    - Date (when test taken)
      - 28/08/2019
    - Course interest
  - File name information:
    - Unique number for each applicant
- **csv - applicant details for a specific month**
  - Key information in file:
    - Applicant name
    - "invited_date" and "month"
      - "invited_date": 28
      - "month": Aug-19
  - File name information:
    - Month and year
- **txt - Sparta Day scores (on a specific date)**
  - Key information in file:
    - Applicant name
    - Date
      - Wednesday 28 August 2019
    - Course interest
  - File name information:
    - Date

### Academy Bucket
- **csv - course and start data scores for people in that cohort**
  - Key information in file:
    - Applicant name
  - File name information:
    - Course name
    - Date (course start date)

**Talent bucket links: applicant name and date**

**Talent to Academy links: applicant name**

## Code for linking together separate documents
File: mongo_atlas_connect
The file above identifies the name of the candidate and allocates a unique ID. It pulls the sparta day results, interview scores and personal info from the Talent collection and the academy scores from the Academy collection. This creates a unique one person view for all of the Sparta Global Information. 


## Uploading new data into the existing database
The runner file Runner.py takes in the data currently in the Talent and Academy collections as well as our new documents. They are put into a Set to identify what is new data anything that is not in the database already will be cleaned and added. 
Example code here: 
documents = list(collection.find())

### Loop through the documents and upload each to S3
for doc in documents:
#### Convert the document to a JSON string
doc_json = dumps(doc)

### Use the '_id' field as the name for the JSON file
file_name = file_name = f"Candidates/{doc['name'].replace(' ', '_')}_{doc['_id']}.json"

### Upload to S3
s3.s3.put_object(Body=doc_json, Bucket=bucket_name, Key=file_name)
print(f"Uploaded {file_name} to S3 bucket {bucket_name}")




License
This project is licensed under the MIT License
