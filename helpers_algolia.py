from algoliasearch.search_client import SearchClient

client = SearchClient.create('YourApplicationID', 'YourAdminAPIKey')
index = client.init_index('your_index_name')


def upload_multiple_records(index, records):
    res = index.save_objects(records, {'autoGenerateObjectIDIfNotExist': True})