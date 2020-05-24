import os
import re
import ast
import time
import json
import pymongo
import datetime
from bs4 import BeautifulSoup

LWM_BASE_URL = "https://www.lordswm.com/"
LOGIN_URL = "login.php"
CLAN_PAGE = "clan_info.php"#
CLAN_LOG_PAGE = "clan_log.php"#
DEFENCE_LOG_PAGE = "clan_mwlog.php"#
PLAYER_PAGE = "pl_info.php"#
PLAYER_TRANSFER_LOG = "pl_transfers.php"#
PLAYER_BATTLE_LOG = "pl_warlog.php"#
PLAYER_CARD_GAME_LOG = "pl_cardlog.php"#
PLAYER_REALITY_LOG = "pl_info_realty.php"#
BATTLE_LINK = "warlog.php"#
CLAN_STATS = "clanstat.php"
TROOP_INFO = "army_info.php"


def return_login_content(user_id, password):
    request_body = {
        "LOGIN_redirect": 0,
        "login": user_id,
        "pass": password,
        "pliv": 12905
    }
    request_header = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return request_header, request_body


def login(s, user_name, password):
    # login
    login_header, login_body = return_login_content(user_name, password)
    login_response = s.post(url=LWM_BASE_URL + LOGIN_URL, headers=login_header, data=login_body)
    print(login_response.status_code)

    # verify login
    soup = BeautifulSoup(login_response.content, 'html.parser')
    if len(soup.find_all('a', href=re.compile(r".*logout.*"))) > 0:
        login_flag = True
    else:
        login_flag = False
    # Retry
    if login_flag:
        return login_flag
    else:
        # login
        login_header, login_body = return_login_content(user_name, password)
        login_response = s.post(url=LWM_BASE_URL + LOGIN_URL, headers=login_header, data=login_body)
        print(login_response.status_code)

        # verify login
        soup = BeautifulSoup(login_response.content, 'html.parser')
        if len(soup.find_all('a', href=re.compile(r".*logout.*"))) > 0:
            login_flag = True
        else:
            login_flag = False
    return login_flag


def get_page_content(s, url):
    page_response = s.get(url)
    return page_response.content


def get_page(s, endpoint):
    """
    :param endpoint: <str>
    """
    url = LWM_BASE_URL + endpoint
    content = get_page_content(s, url)
    return content


def get_character_page(s, player_id):
    """
    :param player_id: <int>
    """
    url = LWM_BASE_URL + PLAYER_PAGE + "?id=" + str(player_id)
    content = get_page_content(s, url)
    return content


def get_battle_log(s, player_id, page=0):
    """
    :param player_id: <int>
    :param page: <int>
    """
    url = LWM_BASE_URL + PLAYER_BATTLE_LOG + "?id=" + str(player_id) + "&page=" + str(page)
    content = get_page_content(s, url)
    return content


def get_card_game_log(s, player_id, page=0):
    """
    :param player_id: <int>
    :param page: <int>
    """
    url = LWM_BASE_URL + PLAYER_CARD_GAME_LOG + "?id=" + str(player_id) + "&page=" + str(page)
    content = get_page_content(s, url)
    return content


def get_transfer_log(s, player_id, page=0):
    """
    :param player_id: <int>
    :param page: <int>
    """
    url = LWM_BASE_URL + PLAYER_TRANSFER_LOG + "?id=" + str(player_id) + "&page=" + str(page)
    content = get_page_content(s, url)
    return content


def get_real_estate_log(s, player_id, page=0):
    """
    :param player_id: <int>
    :param page: <int>
    """
    url = LWM_BASE_URL + PLAYER_REALITY_LOG + "?id=" + str(player_id) + "&page=" + str(page)
    content = get_page_content(s, url)
    return content


def get_clan_page(s, clan_id):
    """
    :param clan_id: <int>
    """
    url = LWM_BASE_URL + CLAN_PAGE + "?id=" + str(clan_id)
    content = get_page_content(s, url)
    return content


def get_clan_log(s, clan_id, page=0):
    """
    :param clan_id: <int>
    :param page: <int>
    """
    url = LWM_BASE_URL + CLAN_LOG_PAGE + "?id=" + str(clan_id) + "&page=" + str(page)
    content = get_page_content(s, url)
    return content


def get_defence_log(s, defence_id, clan_id):
    """
    :param defence_id: <int>
    :param clan_id: <int>
    """
    url = LWM_BASE_URL + DEFENCE_LOG_PAGE + "?key=" + str(defence_id) + "&clan_id=" + str(clan_id)
    content = get_page_content(s, url)
    return content


def get_battle(s, war_id):
    """
    :param war_id: <int>
    """
    url = LWM_BASE_URL + BATTLE_LINK + "?warid=" + str(war_id)
    content = get_page_content(s, url)
    return content
