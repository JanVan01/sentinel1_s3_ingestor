from download.base import BaseDownloader
from download.copernicus import CopernicusDownloader
from search.base import BaseSearch
from search.copernicus import CopernicusSearch
from upload.base import BaseUploader
from upload.s3 import S3Uploader
import credentials

class Ingestor:

    def __init__(self, search: BaseSearch, downloader:BaseDownloader, uploader:BaseUploader):
        self.search = search
        self.downloader = downloader
        self.uploader = uploader

    def ingest(self):
        result = self.search.search()
        path = self.downloader.download(result)
        self.uploader.upload(path)



if __name__ == '__main__':
    search = CopernicusSearch(credentials.copernicus_hub['username'],credentials.copernicus_hub['password'])
    downloader = CopernicusDownloader()
    uploader = S3Uploader()
    ingestor = Ingestor(search, downloader, uploader)
    ingestor.ingest()
