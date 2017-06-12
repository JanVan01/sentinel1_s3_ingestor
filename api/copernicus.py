from api.base import BaseAPI
from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt, InvalidChecksumError

from upload.s3 import S3Uploader
import credentials
import os

INITIAL_DATE = '20170609'

class CopernicusAPI(BaseAPI):
    def __init__(self, user, password, uploader):
        self.__api = SentinelAPI(user=user, password=password)
        self.__uploader = uploader

    def search(self):
        # loading search extend
        footprint = geojson_to_wkt(read_geojson('extend.geojson'))
        results = self.__api.query(area=footprint, initial_date=INITIAL_DATE, platformname='Sentinel-1',
                                   producttype='GRD')
        return results

    # start downloading
    def download(self, products):
        downloadedProducts = []
        for product in products:
            # download product,
            try:
                # save file on local fs
                # verify the downloaded file's integrity by checking its MD5 checksum
                print "downloading %s" % product
                downloadResults = self.__api.download(product, checksum=True)
                # downloadedProducts.append(downloadResults['path'])

                # upload file to s3
                print "uploading %s" % product
                self.upload(downloadResults['path'])

                # remove local file from fs
                print "removing %s" % product
                self.remove(downloadResults['path'])
            except InvalidChecksumError:
                print "ERROR: Invalid checksum, skipping %" % product
        return downloadedProducts

    def upload(self, path):
        self.__uploader.upload(path);

    def remove(self, filename):
        try:
            os.remove(filename)
        except OSError:
            pass