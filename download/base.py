import string


class BaseDownloader:

    def download(self, url: string):
        raise NotImplementedError('This method is not implemented in the base class')