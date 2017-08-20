from api.base import BaseAPI
from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt, InvalidChecksumError, SentinelAPIError

import os


class CopernicusAPI(BaseAPI):
    def __init__(self, user, password):
        super().__init__()
        self.__api = SentinelAPI(user=user, password=password)

    def search(self, start='NOW-7DAYS', end='NOW'):
        self._logger.info('Searching for new data sets')

        # loading search extend
        current_dir = os.path.dirname(__file__)
        extend_path = os.path.join(current_dir, "nrw.geojson")
        footprint = geojson_to_wkt(read_geojson(extend_path))
        try:
            return self.__api.query(area=footprint, initial_date=start, end_date=end, platformname='Sentinel-1', producttype='GRD')
        except SentinelAPIError:
            self._logger.error('There was an error searching for data sets', exc_info=True)
            return {}

    def download(self, product_id):
        self._logger.info("Start downloading product: {}".format(product_id))
        try:
            product_info = self.__api.download(product_id, checksum=True)
            self._logger.info("Product was successfully downloaded to {}".format(product_info['path']))
            return product_info['path']
        except InvalidChecksumError:
            self._logger.error('The checksum of the download was invalid. Skipping product {}').format(product_id)
        except SentinelAPIError:
            self._logger.error('There was an error trying to download the product', exc_info=True)

    def remove(self, filename):
        self._logger.info('Removing product at {}'.format(filename))
        try:
            os.remove(filename)
        except OSError:
            pass
