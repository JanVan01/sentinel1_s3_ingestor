import logging


class BaseUploader:
    def __init__(self):
        self._logger = logging.getLogger('s1_ingestor.upload')

    def upload(self, local_file_path, upload_path):
        raise NotImplementedError('This method is not implemented in the base class')

    def exists(self, path):
        raise NotImplementedError('This method is not implemented in the base class')