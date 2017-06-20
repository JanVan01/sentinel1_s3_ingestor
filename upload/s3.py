import os
import threading
import boto3
import boto3.session
import sys

from boto3.s3.transfer import S3Transfer

import credentials

from upload.base import BaseUploader

AWS_ACCESS_KEY_ID = credentials.aws['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = credentials.aws['AWS_SECRET_ACCESS_KEY']


class S3Uploader(BaseUploader):

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = boto3.client(
            's3',
            region_name='eu-central-1',
            config=boto3.session.Config(signature_version='s3v4'),
            # Hard coded strings as credentials, not recommended.
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    def upload(self, local_file_path, upload_path):
        print("uploading file %s to bucket %s" % (local_file_path, self.bucket_name))
        transfer = S3Transfer(self.client)
        transfer.upload_file(filename=local_file_path, bucket=self.bucket_name, key=upload_path,
                                callback=ProgressPercentage(local_file_path))

    def exists(self, path):
        response = self.client.list_objects(Bucket=self.bucket_name, Prefix=path)
        return 'Content' in response


class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()