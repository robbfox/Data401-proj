# Data401 final project
This project runs an Extract-Transform-Load data pipeline, built in Python. The data consists of various types of information files that are stored in an AWS S3 bucket. The files are in .csv, JSON or .txt format, and contain info about potential and current students at the Sparta Academy. The code uses object-oriented programming, creating classes to inspect the files in S3, read to memory, clean and format the data as required, and load into MongoAtlas, a NoSQL database. 

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


License
This project is licensed under the MIT License