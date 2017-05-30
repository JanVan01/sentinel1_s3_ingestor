from base import BaseSearch
import options

class PepsSearch(BaseSearch):

    def __init__(self):
        search()

    def search(self):
        print('peps search')
        # search in catalog
        search_catalog = 'curl -k -o search.json https://peps.cnes.fr/resto/api/collections/%s/search.json?%s\&startDate=%s\&completionDate=%s\&maxRecords=500' % (options.collection, options.bbox, options.start_date, options.end_date)

        print search_catalog
        os.system(search_catalog)

        return results
