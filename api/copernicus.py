from api.base import BaseAPI
from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt, InvalidChecksumError

import os


class CopernicusAPI(BaseAPI):
    def __init__(self, user, password):
        super().__init__()
        self.__api = SentinelAPI(user=user, password=password)

    def search(self, start='20170101', end='NOW'):
        self._logger.info('Searching for new data sets')

        # loading search extend
        current_dir = os.path.dirname(__file__)
        extend_path = os.path.join(current_dir, "nrw.geojson")
        footprint = geojson_to_wkt(read_geojson(extend_path))
        return self.__api.query(area=footprint, initial_date=start, end_date=end, platformname='Sentinel-1',
                                producttype='GRD')

    def download(self, product_id):
        self._logger.info("Start downloading product: {}".format(product_id))
        try:
            product_info = self.__api.download(product_id, checksum=True)
            self._logger.info("Product was successfully downloaded to {}".format(product_info['path']))
            return product_info['path']
        except InvalidChecksumError:
            self._logger.error('The checksum of the download was invalid skipping product {}').format(product_id)

    def remove(self, filename):
        self._logger.info('Removing product at {}'.format(filename))
        try:
            os.remove(filename)
        except OSError:
            pass
