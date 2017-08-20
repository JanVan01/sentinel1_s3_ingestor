import logging


class Ingestor:
    def __init__(self, api, uploader):
        self.__api = api
        self.__uploader = uploader
        self._logger = logging.getLogger('s1_ingestor.ingestor')

    def ingest(self):
        self._logger.info('Starting the ingestion')
        results = self.__api.search()
        for uuid, details in results.items():
            if not self.__uploader.exists(details['filename']):
                self._logger.info('Product {} does not yet exist'.format(uuid))
                download_path = self.__api.download(uuid)
                if download_path:
                    self.__uploader.upload(download_path, details['filename'])
                    self.__api.remove(download_path)
        self._logger.info('Ingestion Completed')
