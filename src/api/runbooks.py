import adal
import requests
import os
from flask import Flask, request, jsonify, url_for
from flask_restful import Resource, Api
from json import dumps
import autentication
from flask import Blueprint
import setting

runbooks_api = Blueprint('runbooks_api', __name__)

@runbooks_api.route('/runbooks/<subid>/<groupid>/<automationid>/')
def api_get_runbooks(subid,groupid,automationid):
    endpoint = (setting.RUNBOOKS_ENDPOINT % (subid,groupid,automationid))
    headers = {"Authorization": 'Bearer ' + autentication.get_token()}
    json_output = requests.get(endpoint,headers=headers).json()
    return str(json_output)


@runbooks_api.route('/runbooks/<subid>/<groupid>/<automationid>/<runbookid>')
def api_get_runbooks_by_name(subid,groupid,automationid,runbookid):
    endpoint = (setting.RUNBOOK_ENDPOINT % (subid,groupid,automationid,runbookid))
    headers = {"Authorization": 'Bearer ' + autentication.get_token()}
    json_output = requests.get(endpoint,headers=headers).json()
    return str(json_output)

@runbooks_api.route('/runbooks/<subid>/<groupid>/<automationid>/<runbookid>/content')
def api_get_runbook_content(subid,groupid,automationid,runbookid):
    endpoint = (setting.RUNBOOK_CONTENT_ENDPOINT % (subid,groupid,automationid,runbookid))
    headers = {"Authorization": 'Bearer ' + autentication.get_token()}
    json_output = requests.get(endpoint,headers=headers).json()
    return str(json_output)

@runbooks_api.route('/runbooks/<subid>/<groupid>/<automationid>/<runbookid>', methods=['PATCH'])
def api_patch_runbook(subid,groupid,automationid,runbookid):
    obj = request.data.decode('utf8').replace("'", '"')
    print(obj)
    
    endpoint = (setting.RUNBOOK_ENDPOINT % (subid,groupid,automationid,runbookid))
    headers = {"Authorization": 'Bearer ' + autentication.get_token(),"Content-type": "application/json"}
    json_output = requests.patch(endpoint,data=obj,headers=headers).json()
    return str(json_output)


@runbooks_api.route('/runbooks/<subid>/<groupid>/<automationid>/<runbookid>', methods=['PUT'])
def api_put_runbook(subid,groupid,automationid,runbookid):
    obj = request.data.decode('utf8').replace("'", '"')
    print(obj)
    endpoint = (setting.RUNBOOK_ENDPOINT % (subid,groupid,automationid,runbookid))
    headers = {"Authorization": 'Bearer ' + autentication.get_token(),"Content-type": "application/json"}
    json_output = requests.put(endpoint,data=obj,headers=headers).json()
    return str(json_output)

@runbooks_api.route('/runbooks/<subid>/<groupid>/<automationid>/<rubbookid>/<schid>', methods=['POST'])
def api_post_link_runbook_schedule(subid,groupid,automationid,rubbookid,schid):
    # example for the body
    #[{"name":"ResourceGroupName","value":"\"testvms\""},{"name":"VMName","value":"\"*\""}]

    
    obj = request.data.decode('utf8').replace("'", '"')
    print(obj)
    runbook_parameter =  (setting.RUNBOOK_PARAMETER_ENDPOINT % (subid,groupid,automationid,rubbookid))
    schedule_parameter = (setting.SCHEDULE_PARAMETER_ENDPOINT % (subid,groupid,automationid,schid))
    headers = {"Authorization": 'Bearer ' + autentication.get_token(),"Content-type": "text/plain"}
    endpoint_delete = (setting.RUNBOOK_SCHEDULE_DELETE_ENDPOINT % (runbook_parameter.replace("/","%2F"),schedule_parameter.replace("/","%2F")))
    endpoint_post = (setting.RUNBOOK_SCHEDULE_ENDPOINT % (runbook_parameter.replace("/","%2F"),schedule_parameter.replace("/","%2F")))
    
    # We should revisit the code here to make it better
    # run delete first to remove the link
    print(endpoint_delete)
    json_output=requests.post(endpoint_delete,headers=headers).status_code

    #now post
    headers = {"Authorization": 'Bearer ' + autentication.get_token(),"Content-type": "application/json"}
    json_output = requests.post(endpoint_post,data=obj,headers=headers).status_code
    return str(json_output)


@runbooks_api.route('/runbooks/<subid>/<groupid>/<automationid>/<rubbookid>/<schid>', methods=['GET'])
def api_get_link_runbook_schedule(subid,groupid,automationid,rubbookid,schid):
    runbook_parameter =  (setting.RUNBOOK_PARAMETER_ENDPOINT % (subid,groupid,automationid,rubbookid))
    schedule_parameter = (setting.SCHEDULE_PARAMETER_ENDPOINT % (subid,groupid,automationid,schid))
    headers = {"Authorization": 'Bearer ' + autentication.get_token(),"Content-type": "application/json"}
    endpoint = (setting.RUNBOOK_SCHEDULE_PARAMETERS_ENDPOINT % (runbook_parameter.replace("/","%2F"),schedule_parameter.replace("/","%2F")))
    print(endpoint)
    print(autentication.get_token())
    json_output = requests.get(endpoint,headers=headers).json()
    return str(json_output)


@runbooks_api.route('/runbookslinked/<subid>/<groupid>/<automationid>/<rubbookid>', methods=['GET'])
def api_get_link_runbook_schedules(subid,groupid,automationid,rubbookid):
    runbook_parameter =  (setting.RUNBOOK_PARAMETER_ENDPOINT % (subid,groupid,automationid,rubbookid))
    headers = {"Authorization": 'Bearer ' + autentication.get_token(),"Content-type": "application/json"}
    endpoint = (setting.RUNBOOK_SCHEDULES_LIST_ENDPOINT % (runbook_parameter.replace("/","%2F")))
    print(endpoint)
    print(autentication.get_token())
    json_output = requests.get(endpoint,headers=headers).json()
    return str(json_output)


