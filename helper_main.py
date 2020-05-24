import os
import pymongo

import config
import lwm_helpers as lh
import helpers_mongo as hm
import data_extractors as de


def get_clan_info(content):
	"""
		Provides basic info about all clans
	:param content:
	:return:
	"""
	# print("content:", content)
	try:
		clans = content.get("clans", [])
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
	except Exception as e:
		return {"message": str(e)}


def upload_clan_event_data(content):
	"""

	:param content:
	:return:
	"""
	user_name = content.get("user_name", "")
	password = content.get("password", "")
	clan_list = content.get("clan_list", [])
	event_id = content.get("event_id", 0)
	uploaded_records = de.extract_event_performance(user_name, password, clan_list, event_id)
	if uploaded_records is not False:
		return {"records_uploaded": uploaded_records, "clans": clan_list}
	else:
		return {"records_uploaded": 0}


def view_clan_event_data(content):
	"""

	:param content:
	:return:
	"""
	clans = content.get("clan", 1209)
	event_id = content.get("event_id", 1001)
	clan_points = content.get("clan_points", None)
	combat_level = content.get("combat_level", None)
	language = content.get("language", "eng")

	if isinstance(clans, str):
		clan_list = [int(clans)]
	else:
		clan_list = clans

	sorting = list()
	if clan_points is not None:
		sorting.append(("clan_points", int(clan_points)))
	if combat_level is not None:
		sorting.append(("combat_level", int(combat_level)))

	if len(sorting) == 0:
		sorting = [("clan_points", -1), ("combat_level", 1)]

	db_name = "clan"
	col_name = "event_performance"
	search_query = {"clan_id": {"$in": clan_list}, "doctype": "event_performance", "event_id": int(event_id)}
	records_fetched = hm.search_records(
		db_name=db_name,
		col_name=col_name,
		query=search_query,
		fields_required=["player_name", "combat_level", "clan_points", "player_id"],
		sorting_fields=sorting
	)

	with open(os.path.join("templates", "eventPerformance.html"), 'r', encoding='utf-8') as f:
		html_page = f.read()

	if language.lower() == "rus":
		columns = ["герой", "Боевой уровень", "Клановые очки"]
	else:
		columns = ["Player", "Combat level", "Clan Points"]
	table_header = "<tr><th><b>" \
		+ columns[0] + "</b></th><th><b>" \
		+ columns[1] + "</b></th><th><b>" \
		+ columns[2] + "</b></th></tr>"
	table_rows = ""
	for i in records_fetched:
		if language.lower() == "rus":
			player_url = lh.HWM_BASE_URL + lh.PLAYER_PAGE + "?id=" + str(i["player_id"])
		else:
			player_url = lh.LWM_BASE_URL + lh.PLAYER_PAGE + "?id=" + str(i["player_id"])
		table_rows = table_rows + "<tr><td><a href=\"" \
			+ player_url + "\">"\
			+ str(i["player_name"]) + "</a></td><td>" \
			+ str(i["combat_level"]) + "</td><td>" \
			+ str(i["clan_points"]) \
			+ "</td></tr>"

	table = "<div class=\"table-users\"><div class=\"header\">Players</div><table>" \
		+ table_header \
		+ table_rows + "</table></div>"

	# return_page = "<html><body>" + table + "</body></html>"
	return_page = html_page.replace("Stats will come below:", table)
	if language.lower() == "rus":
		return_page = return_page.replace(
			"""<input type="radio" id="eng" name="language" value="eng" checked>""",
			"""<input type="radio" id="eng" name="language" value="eng">"""
		)
		return_page = return_page.replace(
			"""<input type="radio" id="rus" name="language" value="rus">""",
			"""<input type="radio" id="rus" name="language" value="rus" checked>"""
		)
	return return_page
