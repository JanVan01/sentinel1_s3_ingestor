from base64 import b64decode

import logging
import os

from logging.handlers import RotatingFileHandler
from api.copernicus import CopernicusAPI
from upload.s3 import S3Uploader
import credentials
import boto3.session


class Ingestor:
    def __init__(self, api, uploader):
        self.__api = api
        self.__uploader = uploader
        self._logger = logging.getLogger('s1_ingestor.ingestor')

    def ingest(self):
        self._logger.info('Starting the ingestion')
        results = self.__api.search()
        for uuid, details in results.items():
            if not self.__uploader.exists(details['filename']):
                self._logger.info('Product {} does not yet exist'.format(uuid))
                download_path = self.__api.download(uuid)
                if download_path:
                    self.__uploader.upload(download_path, details['filename'])
                    self.__api.remove(download_path)

if __name__ == '__main__':
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
