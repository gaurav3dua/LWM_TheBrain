import os
import json
from flask import Flask, request, render_template, Response, abort

import helper_main as hm

app = Flask(__name__)


@app.route('/api/HealthCheck', methods=['GET'])
def health_check_method():
    """
        Simple GET method to quickly check if app is running. Can be used to switch the app on.
    :return:
    """
    response = {"status": "Success", "message": "The Brain is functioning well!"}
    return Response(json.dumps(response), mimetype='application/json'), 200


@app.route('/api/GetClanInfo', methods=['GET', 'POST'])
def get_clan_info():
    """
        {
            "clans": [] # numbers in the list or empty list for all clans
        }
    :return:
    """
    content = request.json
    response = hm.get_clan_info(content)
    return Response(json.dumps(response), mimetype='application/json'), 200


@app.route('/api/GetEventBattlesInfo', methods=['GET', 'POST'])
def get_event_battle_info():
    """
        {
            "is_clan": <boolean>,
            "clan": <integer>,      # is_clan = True
            "event_name": <string>, # is_clan = True
            "player_id": <integer>  # is_clan = False
        }
    :return: details of the clan / player for the event requested
    """
    content = request.json
    response = hm.get_clan_info(content)
    return Response(json.dumps(response), mimetype='application/json'), 200


@app.route('/cpbCalculator', methods=['GET'])
def get_cpb_calculator():
    """
    :return: returns my cpb calculator html page
    """
    page = "cpbCalculator.html"
    # page = os.path.join("calculators", "cpbCalculator.html")
    return render_template(page)


@app.route('/buyRogues', methods=['POST'])
def buy_troops_rogues():
    """
        {
            "user_id": <string>,    # base64 encoded string $ temporarily normal string
            "password": <string>,   # base64 encoded string $ temporarily normal string
        }
    :return: name, quantity, price of troops bought
    """
    content = request.json
    response = hm.get_clan_info(content)
    return Response(json.dumps(response), mimetype='application/json'), 200


@app.route('/sellRogues', methods=['POST'])
def sell_troops_rogues():
    """
        {
            "user_id": <string>,    # base64 encoded string $ temporarily normal string
            "password": <string>,   # base64 encoded string $ temporarily normal string
        }
    :return: name, quantity, price of troops bought
    """
    content = request.json
    response = hm.get_clan_info(content)
    return Response(json.dumps(response), mimetype='application/json'), 200


@app.route('/api/UploadEventPerformance', methods=['POST'])
def extract_and_upload_clan_event_performance():
    """
        {
            "user_id": <string>,    # base64 encoded string $ temporarily normal string
            "password": <string>,   # base64 encoded string $ temporarily normal string
            "clan_list": <list <int>>,
            "event_id": <int>       # rogues_raids = 1001
        }
    :return:
    """
    content = request.json
    response = hm.upload_clan_event_data(content)
    return Response(json.dumps(response), mimetype='application/json'), 200


@app.route('/api/ViewEventPerformance', methods=['POST'])
def view_clan_event_performance():
    """
        {
            "clan_list": <list <int>>,
            "event_id": <int>,                          # rogues_raids = 1001
            "sorting": <list <tuple <string>, <int>>>   # [("clan_points", -1), ("combat_level", 1)]
        }
    :return:
    """
    content = request.form
    response = hm.view_clan_event_data(content)
    return Response(response, mimetype='text/html'), 200


@app.route('/eventPerformance', methods=['GET'])
def get_event_performance():
    """
    :return: returns my cpb calculator html page
    """
    page = "eventPerformance.html"
    # page = os.path.join("calculators", "cpbCalculator.html")
    return render_template(page)


if __name__ == "__main__": 
    # os.environ.setdefault('PATH', '')
    # Run Flask App
    app.run(host="0.0.0.0", port='4040', debug=True, threaded=True)
