import string

from upload.base import BaseUploader


class S3Uploader(BaseUploader):
    def upload(self, path:string):
        print('uploading the file: {}'.format(path))