import boto3
from botocore.exceptions import NoCredentialsError


class S3Manager:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3')

    def read_file_to_memory(self, s3_key):
        try:
            obj = self.s3.get_object(Bucket=self.bucket_name, Key=s3_key)
            return obj['Body'].read()
        except NoCredentialsError:
            print("Credentials not available")
            return None
        except self.s3.exceptions.NoSuchKey:
            print(f"The object {s3_key} does not exist.")
            return None

    def upload_file(self, local_path, s3_key):
        try:
            self.s3.upload_file(local_path, self.bucket_name, s3_key)
            return True
        except NoCredentialsError:
            print("Credentials not available")
            return False

    def list_files(self, prefix):
        """List all files in a folder"""
        paginator = self.s3.get_paginator('list_objects_v2')
        operation_parameters = {
            'Bucket': self.bucket_name,
            'Prefix': prefix,
        }
        page_iterator = paginator.paginate(PaginationConfig={'MaxItems': 1}, **operation_parameters)
        files = []
        for page in page_iterator:
            print(page)
            #files.append(page)
        #response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix, MaxKeys=1000)
        #files = [obj['Key'] for obj in response.get('Contents', []) if '/' in obj['Key']]
        #sorted_files = [obj['Key'] for obj in files.get('Contents', []) if '/' in obj['Key']]
        return files
