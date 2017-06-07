from api.base import BaseAPI
from api.copernicus import CopernicusAPI
from upload.base import BaseUploader
from upload.s3 import S3Uploader
import credentials


class Ingestor:
    def __init__(self, api: BaseAPI, uploader: BaseUploader):
        self.__api = api
        self.__uploader = uploader

    def ingest(self):
        result = self.__api.search()
        path = self.__api.download(result)
        self.__uploader.upload(path, "path/on/server")


if __name__ == '__main__':
    api = CopernicusAPI(credentials.copernicus_hub['username'], credentials.copernicus_hub['password'])
    uploader = S3Uploader(credentials.s3_bucket['name'])
    ingestor = Ingestor(api, uploader)
    ingestor.ingest()
