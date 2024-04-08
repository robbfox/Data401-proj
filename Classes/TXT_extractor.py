import boto3
import pandas as pd


class TXTExtractor():
    def __init__(self, s3_client=None):
        super().__init__()
        self.s3_client = boto3.client('s3', region_name='eu-central-1')
        self.bucket_name = 'data-eng-401-final-project'
        self.folder_name = 'Talent/'

    def list_txt_files(self):
        """
        List all .txt files in the specified S3 bucket folder
        """
        txt_files = []
        if self.s3_client:
            paginator = self.s3_client.get_paginator('list_objects_v2')
            for page in paginator.paginate(Bucket=self.bucket_name):
                if 'Contents' in page:
                    for obj in page['Contents']:
                        key = obj['Key']
                        if key.endswith('.txt'):
                            txt_files.append(key)
        return txt_files

    def extract(self, file_path):
        if self.s3_client:
            # Check if the file_path exists in the bucket
            if file_path not in self.list_txt_files():
                raise FileNotFoundError(f"File '{file_path}' not found in the S3 bucket.")

            # Read file from S3
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_path)
            text_data = response['Body'].read().decode('utf-8')
        else:
            # Read file locally
            with open(file_path, 'r') as file:
                text_data = file.read()

        print("Text data:", text_data)  # Debugging print

        lines = [line for line in text_data.strip().split("\n") if line.strip()]

        print("Lines:", lines)  # Debugging print

        if len(lines) < 2:
            raise ValueError("Text data does not contain sufficient information")

        # Extract the date and location
        date, location = lines[0], lines[1]

        participants = []
        # Parse participant lines
        for line in lines[2:]:
            name, scores = line.split(" -  ")
            psychometrics, presentation = scores.split(", ")
            psychometrics_score = psychometrics.split(": ")[1]
            presentation_score = presentation.split(": ")[1]
            participants.append(
                {"name": name, "Psychometrics": psychometrics_score, "Presentation": presentation_score})

        # Create a DataFrame
        df = pd.DataFrame(participants)
        df['Date'] = date
        df['Location'] = location
        txt_JSON = df.to_json(orient='records')
        return txt_JSON
