import os


def get_mongo_connection_string():
	"""
		Fetches and Returns mongo db connection string
	:return:
	"""
	mongo_connection_string = os.environ.get("MongoConn")
	return mongo_connection_string


def get_algolia_key():
	"""
		Fetches and Returns algolia api key
	:return:
	"""
	api_key = os.environ.get("AlgoliaKey")
	return api_key


def get_algolia_app_key():
	"""
		Fetches and Returns algolia app id
	:return:
	"""
	app_key = os.environ.get("AlgoliaApp")
	return app_key

