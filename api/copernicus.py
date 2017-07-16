from api.base import BaseAPI
from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt, InvalidChecksumError

import os


class CopernicusAPI(BaseAPI):
    def __init__(self, user, password):
        self.__api = SentinelAPI(user=user, password=password)

    def search(self, start='20170101', end='NOW'):
        # loading search extend
        dir = os.path.dirname(__file__)
	extend_path =  os.path.join(dir, "nrw.geojson")
	footprint = geojson_to_wkt(read_geojson(extend_path))
        return self.__api.query(area=footprint, initial_date=start, end_date=end, platformname='Sentinel-1',
                                producttype='GRD')

    def download(self, product_id):
        try:
            print("downloading %s" % product_id)
            product_info = self.__api.download(product_id, checksum=True)
            return product_info['path']
        except InvalidChecksumError:
            print("ERROR: Invalid checksum, skipping product %s" % product_id)

    def remove(self, filename):
        print("removing %s" % filename)
        try:
            os.remove(filename)
        except OSError:
            pass
