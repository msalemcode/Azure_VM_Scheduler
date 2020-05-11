import os
import adal
import requests
from flask import Flask, request, jsonify, url_for
from flask_restful import Resource, Api
from json import dumps
import subscriptions 
import jobs
import runbooks
import schedules
import automation
import user
import setting
import time
app = Flask(__name__)


app.register_blueprint(subscriptions.subscriptions_api)
app.register_blueprint(jobs.jobs_api)
app.register_blueprint(runbooks.runbooks_api)
app.register_blueprint(schedules.schedules_api)
app.register_blueprint(automation.automation_api)
app.register_blueprint(user.user_api)


@app.route('/')
def api_root():
	#print("REQUEST time : ", request.args.get('time'))
	return 'Welcome' 

if __name__ == '__main__':
	print("server time : ", time.strftime('%A %B, %d %Y %H:%M:%S %Z'))
	setting.load_kv_values()
	app.run(host='0.0.0.0', port=5000)

    
