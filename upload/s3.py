import boto3
import sys
import credentials
import os

from upload.base import BaseUploader

AWS_ACCESS_KEY_ID = credentials.aws['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = credentials.aws['AWS_SECRET_ACCESS_KEY']

class S3Uploader(BaseUploader):

    def __init__(self, bucket_name):
        #self.conn = boto.connect_s3(AWS_ACCESS_KEY_ID,  AWS_SECRET_ACCESS_KEY, host="s3-eu-central-1.amazonaws.com")
        self.bucket_name = bucket_name
        self.client = boto3.client(
            's3',
            # Hard coded strings as credentials, not recommended.
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

    def upload(self, local_file_path, upload_path=''):
        upload_path = local_file_path[-71:]
        # TODO: check if file exists on bucket
        #print self.s3.Object(self.bucket_name, upload_path).put(Body = open(local_file_path, 'rb'))
        print "uploading %s to %s bucket" % (local_file_path, self.bucket_name)

        self.client.upload_file(local_file_path, self.bucket_name, upload_path)

        # bucket = self.conn.get_bucket(self.bucket_name, validate=False)
        # key = boto.s3.key.Key(bucket, local_file_path)
        # with open(local_file_path) as f:
        #     key.send_file(f, cb=self.percent_cb, num_cb=10)


    def exists(self, path):
        bucket = self.s3.Bucket(self.bucket_name)
        return len(list(bucket.objects.filter(Prefix=path))) > 0

        #try:
        #    self.s3.Object(self.bucket, path).load()
        #except botocore.exceptions.ClientError:
        #    return False
        #return True

    def percent_cb(self, complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()

    def mycb(self, so_far, total):
        print '%d bytes transferred out of %d' % (so_far, total)
