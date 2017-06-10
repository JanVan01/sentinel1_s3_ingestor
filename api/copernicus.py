from api.base import BaseAPI
from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt, InvalidChecksumError
import requests

INITIAL_DATE = '20170609'


class CopernicusAPI(BaseAPI):
    def __init__(self, user, password):
        self.__api = SentinelAPI(user=user, password=password)

    def search(self):
        print('copernicus api')
        print('reading extend...')
        footprint = geojson_to_wkt(read_geojson('extend.geojson'))
        print('getting search results...')
        results = self.__api.query(footprint, initial_date=INITIAL_DATE, platformname='Sentinel-1',
                                   producttype='GRD')

        return results

    # start downloading
    def download(self, products):
        downloadedProducts = []
        for product in products:
            # download product,
            try:
                # verify the downloaded file's integrity by checking its MD5 checksum
                downloadResults = self.__api.download(product, checksum=True)
                downloadedProducts.append(downloadResults['path'])
            except InvalidChecksumError:
                print "ERROR: Invalid checksum, skipping %" % product
        return downloadedProducts