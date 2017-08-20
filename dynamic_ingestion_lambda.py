import boto3

import credentials
from sentinel_s3_ingestor.api import CopernicusAPI
from sentinel_s3_ingestor.upload.s3 import S3Uploader

api = CopernicusAPI(credentials.copernicus_hub['username'], credentials.copernicus_hub['password'])
uploader = S3Uploader(credentials.s3_bucket['name'])


def start_instance(instance_id):
    print("starting the instance")
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instance_id)
    if instance.state['Name'] != 'running':
        instance.start()


def handler(event, context):
    print('searching for data sets')
    results = api.search()
    for uuid, details in results.items():
        if not uploader.exists(details['filename']):
            start_instance(credentials.ec2_instance['id'])
            break
