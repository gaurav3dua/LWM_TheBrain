import os

import environment_variables

def get_mongo_connection_string():
	mongo_connection_string = os.environ.get("MongoConn", environment_variables.MongoConn)
	return mongo_connection_string