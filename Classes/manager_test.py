from s3_manager import *

s3 = S3Manager("data-eng-401-final-project")
lst = s3.list_files("Talent/")
for file in lst:
    print(file)

# s3.upload_file("hello.txt", "Academy/hello_test")

# paginator = s3.get_paginator('list_objects_v2')
# pages = paginator.paginate(Bucket='bucket', Prefix='prefix')
#
# for page in pages:
#     for obj in page['Contents']:
#         print(obj['Size'])