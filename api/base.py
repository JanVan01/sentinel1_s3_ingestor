class BaseAPI:
    def search(self):
        raise NotImplementedError("This method is not implemented in the base class")

    def download(self, path):
        raise NotImplementedError("This method is not implemented in the base class")

    def remove(self, filename):
        raise NotImplementedError("This method is not implemented in the base class")
