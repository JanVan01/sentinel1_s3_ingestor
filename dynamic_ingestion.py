import logging
import os
from base64 import b64decode
from logging.handlers import RotatingFileHandler

import boto3

import credentials
from sentinel_s3_ingestor.api.copernicus import CopernicusAPI
from sentinel_s3_ingestor.ingestor import Ingestor
from sentinel_s3_ingestor.upload.s3 import S3Uploader

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

working_dir = os.path.dirname(__file__)
log_file = os.path.join(working_dir, 'log.txt')
file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount= 5)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logging.basicConfig(handlers=[console_handler, file_handler], level=logging.INFO)

# suppress logging messages from libraries
logging.getLogger('boto3').propagate = False
logging.getLogger('botocore').propagate = False
logging.getLogger('sentinelsat').propagate = False

uploader = S3Uploader(credentials.s3_bucket['name'])
api = CopernicusAPI(credentials.copernicus_hub['username'], credentials.copernicus_hub['password'])
ingestor = Ingestor(api, uploader)

# broad exception handler to handle all exceptions not
# specifically handled before, allowing the instance to
# shut down uninterrupted
try:
    ingestor.ingest()
except Exception:
    logging.error('There was an error in the ingestion. The instance will shut down now')

ec2 = boto3.resource('ec2', region_name="eu-central-1")
instance = ec2.Instance(credentials.ec2_instance['id'])

if 'Value' in instance.describe_attribute(Attribute='userData')['UserData']:
    user_data = b64decode(instance.describe_attribute(Attribute='userData')['UserData']['Value']).decode('utf-8')
else:
    user_data = ''

if user_data != 'dev':
    logging.getLogger(__name__).info('Shutting down instance')
    instance.stop()