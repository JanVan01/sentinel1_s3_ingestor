import string

import boto3
import botocore

from upload.base import BaseUploader


class S3Uploader(BaseUploader):

    def __init__(self, bucket_name:string):
        self.s3 = boto3.resource('s3')
        self.bucket_name = bucket_name

    def upload(self, local_file_path:string, upload_path:string):
        self.s3.Object(self.bucket_name, upload_path).put(Body = open(local_file_path, 'rb'))

    def exists(self, path):
        bucket = self.s3.Bucket(self.bucket_name)
        return len(list(bucket.objects.filter(Prefix=path))) > 0

        #try:
        #    self.s3.Object(self.bucket, path).load()
        #except botocore.exceptions.ClientError:
        #    return False
        #return True
