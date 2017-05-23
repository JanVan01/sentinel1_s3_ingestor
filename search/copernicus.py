from search.base import BaseSearch
from sentinelsat.sentinel import SentinelAPI


COORDINATES = '7.504775917047763 51.86355368445314,7.79033340014175 51.86355368445314,7.79033340014175 ' \
              '52.036805704597015,7.504775917047763 52.036805704597015,7.504775917047763 51.86355368445314 '


class CopernicusSearch(BaseSearch):

    def __init__(self, user, password):
        self.api = SentinelAPI(user=user, password=password)

    def search(self):
        print('copernicus search')
        results = self.api.query(area=COORDINATES)

        return results
