from bs4 import BeautifulSoup

import lwm_helpers as lh


def players_in_clan(s, clan_id):
    """
    :param s: <session object>
    :param clan_id: <int>
    """
    clan_page_content = lh.get_clan_page(s, clan_id)
    clan_soup = BeautifulSoup(clan_page_content, features="lxml")
    players = clan_soup.find_all("table", {"class": "wb", "width": "80%"})[1].find_all("tr")
    return players


def scan_players_on_clan_page_for_event(event_id, clan_id, players):
    """
    :param event_id: <int>
    :param clan_id: <int>
    :param players: <list <soup>>
    """
    event_scores = list()
    for player in players:
        player_data = player.find_all("td")
        if ".gif" in str(player_data[1]):
            player_id_index = 2
            player_name_index = 2
            player_combat_level_index = 3
            event_points_index = 5
        else:
            player_id_index = 1
            player_name_index = 1
            player_combat_level_index = 2
            event_points_index = 4
        player_id = int(player_data[player_id_index].find_all("a")[0]["href"].split('=')[1])
        player_name = player_data[player_name_index].find_all("a")[0].text
        player_combat_level = int(player_data[player_combat_level_index].text)
        try:
            event_points = player_data[event_points_index].find_all("font")
        except:
            event_points = []
        if len(event_points) > 0:
            event_points = int(event_points[0].text.replace(",", ""))
        else:
            event_points = 0
        event_data = {
            "doctype": "event_performance",
            "event_id": event_id,
            "clan_id": clan_id,
            "player_id": player_id,
            "player_name": player_name,
            "combat_level": player_combat_level,
            "clan_points": event_points
        }
        event_scores.append(event_data)
    return event_scores
