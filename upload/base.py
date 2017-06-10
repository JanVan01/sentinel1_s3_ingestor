import string


class BaseUploader:

    def upload(self, local_file_path, upload_path):
        raise NotImplementedError('This method is not implemented in the base class')

    def exists(self, path):
        raise NotImplementedError('This method is not implemented in the base class')