from api.copernicus import CopernicusAPI
from upload.s3 import S3Uploader
import credentials


class Ingestor:
    def __init__(self, api, uploader):
        self.__api = api
        self.__uploader = uploader

    def ingest(self):
        results = self.__api.search()
        for uuid, details in results.items():
            if not self.__uploader.exists(details['filename']):
                print('file %s does not yet exist' % details['filename'])
                download_path = self.__api.download(uuid)
                self.__uploader.upload(download_path, details['filename'])
                self.__api.remove(download_path)


if __name__ == '__main__':
    uploader = S3Uploader(credentials.s3_bucket['name'])
    api = CopernicusAPI(credentials.copernicus_hub['username'], credentials.copernicus_hub['password'])
    ingestor = Ingestor(api, uploader)
    ingestor.ingest()
