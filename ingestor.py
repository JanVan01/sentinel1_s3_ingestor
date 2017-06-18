from api.base import BaseAPI
from api.copernicus import CopernicusAPI
from upload.base import BaseUploader
from upload.s3 import S3Uploader
import credentials


class Ingestor:
    def __init__(self, api):
        self.__api = api
        self.__uploader = uploader

    def ingest(self):
        result = self.__api.search()
        self.__api.download(result)


if __name__ == '__main__':
    uploader = S3Uploader(credentials.s3_bucket['name'])
    api = CopernicusAPI(credentials.copernicus_hub['username'], credentials.copernicus_hub['password'], uploader)
    ingestor = Ingestor(api)
    ingestor.ingest()
