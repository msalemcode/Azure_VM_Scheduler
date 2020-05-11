import logging
import os
import subprocess
import sys
from .models import Subscription,VMlist
from home import setting
import requests
import json
from account import auth, token_cache, settings as auth_settings

def list_subscriptions():
    r=requests.get(setting.REST_API_ENDPOINT+'/subscriptions/')
    print(r.status_code)
    r.headers['content-type']='application/json; charset=utf8'
    json_output=json.loads(r.text.replace("'","\"")).get('value')
    print(str(json_output))
    return (json_output)



def get_valid_subscription(request,mysubscriptions,userid):

    #groupclient = get_client_from_cli_profile(ResourceManagementClient)
    print("Get Valid Subscription")
    print(mysubscriptions)
    sublist = []
    for l in mysubscriptions:
        sublist.append(Subscription(l['subscriptionId'],l['subscriptionId'],l['displayName']))
    print("New Formated sub")
    print(sublist)
    return sublist 
        
        #print(setting.REST_API_ENDPOINT+'/user/'+l['subscriptionId']+'/'+userid)
        #rest=request.get(setting.REST_API_ENDPOINT+'/user/'+l['subscriptionId']+'/'+userid).text
        #print(rest)
        #if (rest != "{}"):
        #    sublist.append(Subscription(l['subscriptionId'],l['subscriptionId'],l['displayName']))

       
def get_resourcegroup_vmlist(subid,groupid):
    r=requests.get(setting.REST_API_ENDPOINT+'/subscriptions/'+subid+'/resourcegroups/'+groupid+'/vmlist')
    rlist=r.text.replace(')','').replace('(','').replace("'",'').split(', ')
    vmlist=[['*','All']]
    for v in rlist:
        l=[]
        l.append(v)
        l.append(v)

        vmlist.append(l)
 
    return vmlist

#'/subscriptions/<subid>/resourcegroups/<groupid>/vmstatus',
def get_resourcegroup_vmstatus():
    endpoint=setting.REST_API_ENDPOINT+'/subscriptions/'+setting.SUBSCRIPTION_ID+'/resourcegroups/'+setting.CURRENT_RESOURCE_GROUP+'/vmstatus'
    r=requests.get(endpoint).json()
    print(r)
    return r

def post_vm_action(request,rg,vm,action):
    #('/subscriptions/<subid>/resourcegroups/<groupid>/<vmid>/<action>/<token>',methods=['POST'])
    endpoint=setting.REST_API_ENDPOINT+'/subscriptions/'+setting.SUBSCRIPTION_ID+'/resourcegroups/'+setting.CURRENT_RESOURCE_GROUP+'/'+vm+'/'+action

    print(endpoint)
    r=requests.post(endpoint)
    print(r)
    return r