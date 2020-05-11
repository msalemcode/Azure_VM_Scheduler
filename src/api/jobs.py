import adal
import requests
import os
from flask import Flask, request, jsonify, url_for
from flask_restful import Resource, Api
from json import dumps
import autentication
from flask import Blueprint
import setting
jobs_api = Blueprint('jobs_api', __name__)

@jobs_api.route('/jobs/<subid>/<groupid>/<automationid>')
def api_get_jobs(subid,groupid,automationid):
    endpoint = (setting.JOBS_ENDPOINT % (subid,groupid,automationid))
    headers = {"Authorization": 'Bearer ' + autentication.get_token()}
    json_output = requests.get(endpoint,headers=headers).json()
    return str(json_output)

@jobs_api.route('/jobs/<subid>/<groupid>/<automationid>/<jobid>', methods=["GET"])
def api_get_job(subid,groupid,automationid,jobid):
    endpoint2 = (setting.JOB_ENDPOINT % (subid,groupid,automationid,jobid))
    headers = {"Authorization": 'Bearer ' + autentication.get_token()}
    json_output = requests.get(endpoint2,headers=headers).json()
    return str(json_output)


@jobs_api.route('/jobs/<subid>/<groupid>/<automationid>/<jobid>', methods=["PUT"])
def api_put_newjob(subid,groupid,automationid,jobid):
    obj = request.data.decode('utf8').replace("'", '"')
    print (obj)
    endpoint = (setting.JOB_ENDPOINT % (subid,groupid,automationid,jobid))
    print(endpoint)
    headers = {"Authorization": 'Bearer ' + autentication.get_token(),"Content-type": "application/json"}
    json_output = requests.put(endpoint,data=obj,headers=headers).json()
    return str(json_output)


@jobs_api.route('/jobs/<subid>/<groupid>/<automationid>/<jobid>/<controlid>', methods=["POST"])
def api_post_control_job(subid,groupid,automationid,jobid,controlid):
    
    control_list = ['stop', 'resume', 'suspend']
    ops = str(controlid).lower()
    if any( ops in s for s in control_list):
        endpoint = (setting.JOB_CONTROL_ENDPOINT % (subid,groupid,automationid,jobid,ops))
        print(endpoint)
        headers = {"Authorization": 'Bearer ' + autentication.get_token(),"Content-type": "application/json"}
        output = str(requests.post(endpoint,headers=headers))
        return (output)
    else:
        return str("Stop, Resume and Suspended are the only valid operations")


'''
Job Schedule API
'''
@jobs_api.route('/jobschedule/<subid>/<groupid>/<automationid>')
def api_get_Listjobschedule(subid,groupid,automationid):
    endpoint = (setting.JOB_SCHEDULES_ENDPOINT % (subid,groupid,automationid))
    headers = {"Authorization": 'Bearer ' + autentication.get_token()}
    json_output = requests.get(endpoint,headers=headers).json()
    return str(json_output)


@jobs_api.route('/jobschedule/<subid>/<groupid>/<automationid>/<jobid>')
def api_get_jobscheduledetail(subid,groupid,automationid,jobid):
    endpoint = (setting.JOB_SCHEDULE_ENDPOINT % (subid,groupid,automationid,jobid))
    headers = {"Authorization": 'Bearer ' + autentication.get_token()}
    json_output = requests.get(endpoint,headers=headers).json()
    return str(json_output)