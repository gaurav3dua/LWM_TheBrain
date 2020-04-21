import os

def get_mongo_connection_string():
	mongo_connection_string = os.environ.get("MongoConn")
	return mongo_connection_string