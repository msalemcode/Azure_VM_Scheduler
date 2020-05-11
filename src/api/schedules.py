import adal
import requests
import os
from flask import Flask, request, jsonify, url_for
from flask_restful import Resource, Api
from json import dumps
import autentication
from flask import Blueprint
import setting

schedules_api = Blueprint('schedules_api', __name__)

@schedules_api.route('/schedules/<subid>/<groupid>/<automationid>')
def api_get_schedules(subid,groupid,automationid):
    endpoint = (setting.SCHEDULES_ENDPOINT % (subid,groupid,automationid))
    headers = {"Authorization": 'Bearer ' + autentication.get_token()}
    json_output = requests.get(endpoint,headers=headers).json()
    return str(json_output)

@schedules_api.route('/schedules/<subid>/<groupid>/<automationid>/<schid>')
def api_get_schedules_by_id(subid,groupid,automationid,schid):
    endpoint = (setting.SCHEDULE_ENDPOINT % (subid,groupid,automationid,schid))
    headers = {"Authorization": 'Bearer ' + autentication.get_token()}
    json_output = requests.get(endpoint,headers=headers).json()
    return str(json_output)


@schedules_api.route('/schedules/<subid>/<groupid>/<automationid>/<schid>', methods=['PUT'])
def api_put_schedule(subid,groupid,automationid,schid):
    obj = request.data.decode('utf8').replace("'", '"')
    print("Reciving the following body")
    print(obj)
    print("")
    endpoint = (setting.SCHEDULE_ENDPOINT % (subid,groupid,automationid,schid))
    headers = {"Authorization": 'Bearer ' + autentication.get_token(),"Content-type": "application/json"}
    json_output = requests.put(endpoint,data=obj,headers=headers).json()
    print(json_output)
    return str(json_output)

@schedules_api.route('/schedules/<subid>/<groupid>/<automationid>/<schid>', methods=['PATCH'])
def api_patch_schedule(subid,groupid,automationid,schid):
    obj = request.data.decode('utf8').replace("'", '"')
    print(obj)
    endpoint = (setting.SCHEDULE_ENDPOINT % (subid,groupid,automationid,schid))
    headers = {"Authorization": 'Bearer ' + autentication.get_token(),"Content-type": "application/json"}
    json_output = requests.patch(endpoint,data=obj,headers=headers).json()
    return str(json_output)

@schedules_api.route('/schedules/<subid>/<groupid>/<automationid>/<schid>', methods=["DELETE"])
def api_delete_schedules(subid,groupid,automationid,schid):
    
    endpoint = (setting.SCHEDULE_ENDPOINT % (subid,groupid,automationid,schid))
    headers = {"Authorization": 'Bearer ' + autentication.get_token()}
    json_output = requests.delete(endpoint,headers=headers).json()
    return str(json_output)

   