import boto3
import boto3.session
import credentials

from upload.base import BaseUploader

AWS_ACCESS_KEY_ID = credentials.aws['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = credentials.aws['AWS_SECRET_ACCESS_KEY']

class S3Uploader(BaseUploader):

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3 = boto3.resource(
            's3',
            region_name='eu-central-1',
            config=boto3.session.Config(signature_version='s3v4'),
            # Hard coded strings as credentials, not recommended.
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

    def upload(self, local_file_path, upload_path=''):
        upload_path = local_file_path[-71:]
        # TODO: check if file exists on bucket
        print("uploading file %s to bucket %s" % (local_file_path, self.bucket_name))
        self.s3.Object(self.bucket_name, upload_path).put(Body=open(local_file_path, 'rb'))

    def exists(self, path):
        bucket = self.s3.Bucket(self.bucket_name)
        return len(list(bucket.objects.filter(Prefix=path))) > 0
