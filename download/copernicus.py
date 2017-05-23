import string

from download.base import BaseDownloader


class CopernicusDownloader(BaseDownloader):

    def download(self, url: string):
        print('downloading the file at: {}'.format(url))
        return 'path/to/file'