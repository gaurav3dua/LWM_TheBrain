import pymongo

import config

def get_clan_info(content):
	"""
	Provides basic info about all clans
	"""
	# print("content:", content)
	clans = content.get("clans") or []
	conn_string = config.get_mongo_connection_string()
	if conn_string is None:
		return {
			"conn_string": conn_string,
			"type": str(type(conn_string)),
			"message": "mongo conn_string not set"
		}
	# print(conn_string)
	client = pymongo.MongoClient(conn_string)
	# print("connected to server")
	db = client['clan']
	# print("connected to db")
	col = db['clan_info']
	# print("connected to collection")
	if len(clans) == 0:
		query = {}
	else:
		query = {"clan_id": {"$in": clans}}
	# print("query:", query)
	try:
		records = col.find(query).sort("clan_id")
	except:
		return {
			"conn_string": conn_string,
			"type": str(type(conn_string)),
			"message": "could not fetch from mongo"
		}
	# print("records:", records)
	clan_records = list()
	for record in records:
		del record["_id"]
		# print(record)
		clan_records.append(record)
	# print(len(clan_records))
	return clan_records