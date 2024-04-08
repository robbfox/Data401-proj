import boto3
import json


class JSONExtractor():
    def __init__(self, s3_client=None):
        super().__init__()
        self.s3_client = s3_client or boto3.client('s3')
        self.bucket_name = 'data-eng-401-final-project'
        self.file_path = 'Talent/'

    def extract(self):
        # List objects
        response = self.s3_client.list_objects_v2(
            Bucket=self.bucket_name,
            Prefix=self.file_path
        )

        # Extract JSON files and their contents from the list of objects
        json_contents = []
        if 'Contents' in response:
            for obj in response['Contents']:
                key = obj['Key']
                # Check if the object is a JSON file
                if key.endswith('.json'):
                    # Download the JSON file
                    file_obj = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
                    # Read and decode the file content
                    file_content = file_obj['Body'].read().decode('utf-8')
                    # Parse the JSON content and add it to the list
                    json_contents.append(json.loads(file_content))

        return json_contents
