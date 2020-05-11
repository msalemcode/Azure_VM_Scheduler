import adal
import requests
import os
from flask import Flask, request, jsonify, url_for
from flask_restful import Resource, Api
from json import dumps
import autentication
from flask import Blueprint
import setting
import json
import logging
import os
import subprocess
import sys
import objectpath
from azure.mgmt.resource import SubscriptionClient


from knack.util import CLIError

_GREEN = "\033[0;32m"
_BOLD = "\033[;1m"


subscriptions_api = Blueprint('subscriptions_api', __name__)

@subscriptions_api.route('/subscriptions/')
def api_subscriptions():
    endpoint = setting.SUBSCRIPTIONS_ENDPOINT
    headers = {"Authorization": 'Bearer ' + autentication.get_token()}
    json_output = requests.get(endpoint,headers=headers).json()
    # get all the subscription
    
    return str(json_output)

@subscriptions_api.route('/subscriptions/<subid>/resourcegroups')
def api_resourcegroups(subid):
    endpoint = (setting.RESOURCEGROUPS_ENDPOINT % (subid))
    headers  = {"Authorization": 'Bearer ' + autentication.get_token()}
    json_output = requests.get(endpoint,headers=headers).json()
    return str(json_output)

@subscriptions_api.route('/subscriptions/<subid>/resourcegroups/<groupid>')
def api_resourcegroupInfo(subid,groupid):
    endpoint = (setting.RESOURCEGROUP_ENDPOINT % (subid,groupid))
    headers  = {"Authorization": 'Bearer ' + autentication.get_token()}
    json_output = requests.get(endpoint,headers=headers).json()
    return str(json_output)


@subscriptions_api.route('/subscriptions/<subid>/resourcegroups/<groupid>/<roleid>',methods=['GET'])
def api_resourcegroupRole(subid,groupid,roleid):
    endpoint = (setting.RESOURCEGROUP_ENDPOINT % (subid,groupid,roleid))
    headers  = {"Authorization": 'Bearer ' + autentication.get_token(),"Content-type": "application/json"}
    json_output = requests.get(endpoint,headers=headers).json()
    return (json_output)    


@subscriptions_api.route('/subscriptions/<subid>/resourcegroups/<groupid>/vmlist',methods=['GET'])
def api_resourcegroup_vmlist(subid,groupid):
    endpoint = (setting.RESOURCEGROUP_VMS_ENDPOINT % (subid,groupid))
    #print(headers)
    headers  = {"Authorization": 'Bearer ' + autentication.get_token(),"Content-type": "application/json"}
    json_output = requests.get(endpoint,headers=headers).json()
    vms=json.dumps(json_output)
    #vms = str(json_output).replace("'","\"").replace("True","\"True\"").replace("False","\"False\"")
    vms_json=json.loads(vms)
    vms_data = objectpath.Tree(vms_json['value'])
    namelist = tuple(vms_data.execute('$.name'))
    print(namelist)
    return str(namelist) 


@subscriptions_api.route('/subscriptions/<subid>/resourcegroups/<groupid>/vmstatus',methods=['GET'])
def api_resourcegroup_vmlist_status(subid,groupid):
    endpoint = (setting.RESOURCEGROUP_VMS_ENDPOINT % (subid,groupid))
    #print(headers)
    headers  = {"Authorization": 'Bearer ' + autentication.get_token(),"Content-type": "application/json"}
    json_output = requests.get(endpoint,headers=headers).json()
    vms=json.dumps(json_output)
    #vms = str(json_output).replace("'","\"").replace("True","\"True\"").replace("False","\"False\"")
    vms_json=json.loads(vms)
    vms_data = objectpath.Tree(vms_json['value'])
    namelist = tuple(vms_data.execute('$.name'))
    print("========= vm list name =================")
    print(namelist)
    print ("============vm status end point =======")
    print(setting.RESOURCEGROUP_VM_STATUS_ENDPOINT)
    vmstatus=[]
    for vm in namelist:
        print("processing vm" + vm)
        endpoint = (setting.RESOURCEGROUP_VM_STATUS_ENDPOINT % (subid,groupid,vm))
        headers  = {"Authorization": 'Bearer ' + autentication.get_token(),"Content-type": "application/json"}
        json_output = requests.get(endpoint,headers=headers).json()
        detail=json.dumps(json_output)
        #detail = str(json_output).replace("'","\"").replace("True","\"True\"").replace("False","\"False\"")
        print(detail)
        vm_json=json.loads(detail)
        print(json)
        namelist = vm_json["properties"]["instanceView"]["statuses"][1]["code"]
        print(namelist)
        #namelist = tuple(status.execute('$.instanceView.statuses.code'))
        if "PowerState/running" in namelist:
            vmstatus.append({'vm_name':vm,'status':'running'})
        else:
            vmstatus.append({'vm_name':vm,'status':'stopped'})

        result=json.dumps(vmstatus)

    return result

@subscriptions_api.route('/subscriptions/<subid>/resourcegroups/<groupid>/<vmid>/<action>',methods=['POST'])
def api_resourcegroup_vm_manage(subid,groupid,vmid,action):
    if(action=="start"):
        endpoint = (setting.RESOURCEGROUP_VM_START_ENDPOINT % (subid,groupid,vmid))

    if(action=="stop"):   
        endpoint = (setting.RESOURCEGROUP_VM_STOP_ENDPOINT % (subid,groupid,vmid))

    if(action=="restart"):   
        endpoint = (setting.RESOURCEGROUP_VM_RESTART_ENDPOINT % (subid,groupid,vmid))

    headers  = {"Authorization": 'Bearer ' + autentication.get_token(),"Content-type": "application/json"}
    print(endpoint)
    json_output = requests.post(endpoint,headers=headers).status_code
    return str(json_output)

