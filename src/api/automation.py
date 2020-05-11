import adal
import requests
import os
from flask import Flask, request, jsonify, url_for
from flask_restful import Resource, Api
from json import dumps
import autentication
from flask import Blueprint
import setting

automation_api = Blueprint('automation_api', __name__)

@automation_api.route('/automation/<subid>/<groupid>/<automationid>/')
def api_get_automation(subid,groupid,automationid):
    print(setting.AUTOMATION_ENDPOINT)
    #endpoint = (autentication.kv_get_secret("automation-endpoint") % (subid,groupid,automationid))
    endpoint = (setting.AUTOMATION_ENDPOINT % (subid,groupid,automationid))
    headers = {"Authorization": 'Bearer ' + autentication.get_token()}
    json_output = requests.get(endpoint,headers=headers).json()
    return str(json_output)


