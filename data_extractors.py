import requests

import lwm_helpers as lh
import clan_helpers as ch
import helpers_mongo as hm


def extract_event_performance(user_name, password, clan_list, event_id):
    """

    :param user_name: <string>
    :param password: <string>
    :param clan_list: <list <string>>
    :param event_id: <int>
    :return:
    """
    total_uploads = 0
    s = requests.Session()

    login_flag = lh.login(s, user_name, password)
    print("Login flag:", login_flag)
    if login_flag:
        print("Clan List:", clan_list)
        for clan_id in clan_list:
            print("Clan_ID:", clan_id)
            players = ch.players_in_clan(s, clan_id)
            clan_performance = ch.scan_players_on_clan_page_for_event(event_id, clan_id, players)
            print("Num of records in clan_performance:", len(clan_performance))

            db_name = "clan"
            col_name = "event_performance"

            delete_query = {"clan_id": clan_id, "doctype": "event_performance", "event_id": event_id}
            deleted_old_records = hm.delete_records_by_query(db_name, col_name, delete_query)
            uploaded_records = hm.upload_records(db_name, col_name, clan_performance)

            total_uploads += len(clan_performance)
        print("Total Uploads:", total_uploads)
        return total_uploads
    else:
        return False
