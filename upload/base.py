import string


class BaseUploader:

    def upload(self, path:string):
        raise NotImplementedError('This method is not implemented in the base class')

    def exists(self, name):
        raise NotImplementedError('This method is not implemented in the base class')