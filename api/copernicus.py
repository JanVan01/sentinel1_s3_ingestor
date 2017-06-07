from api.base import BaseAPI
from sentinelsat.sentinel import SentinelAPI

COORDINATES = '5.497222679018508 50.145373303201524,10.066142408522333 50.145373303201524,10.066142408522333 ' \
              '52.60662673233318,5.497222679018508 52.60662673233318,5.497222679018508 50.145373303201524 '

INITIAL_DATE = '20160101'


class CopernicusAPI(BaseAPI):
    def __init__(self, user, password):
        self.__api = SentinelAPI(user=user, password=password)

    def search(self):
        print('copernicus api')
        results = self.__api.query(area=COORDINATES, initial_date=INITIAL_DATE, platformname='Sentinel-1',
                                   producttype='GRD')

        return results

    def download(self, url):
        print('downloading the file at: {}'.format(url))
        return 'path/to/file'
