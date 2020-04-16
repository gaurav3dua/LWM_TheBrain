import time
import json
from flask import Flask, request, render_template, Response, abort

import helper_main as hm


app = Flask(__name__)


@app.route('/api/HealthCheck', methods=['GET'])
def health_check_method():
    """
        
    :return:
    """
    response = {
    	"status": "Success",
    	"message": "The Brain is functioning well!"
    }
    return Response(json.dumps(response), mimetype='application/json'), 200


@app.route('/api/GetClanInfo', methods=['POST'])
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


if __name__ == "__main__":
    # Run Flask App
    app.run(host="0.0.0.0", port='4040', debug=False, threaded=True)
