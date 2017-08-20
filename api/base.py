import logging

class BaseAPI:
    def __init__(self):
        self._logger = logging.getLogger("s1_ingestor.api")

    def search(self):
        raise NotImplementedError("This method is not implemented in the base class")

    def download(self, path):
        raise NotImplementedError("This method is not implemented in the base class")

    def remove(self, filename):
        raise NotImplementedError("This method is not implemented in the base class")
