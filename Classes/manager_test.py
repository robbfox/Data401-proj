from s3_manager import *

s3 = S3Manager("data-eng-401-final-project")
lst = s3.list_files("Talent/")
for file in lst:
    print(file)
