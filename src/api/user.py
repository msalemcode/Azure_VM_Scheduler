import os
import json
from datetime import datetime
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient, SubscriptionClient
from azure.common.credentials import UserPassCredentials
from azure.mgmt.authorization import AuthorizationManagementClient
import autentication
import requests

from flask import Blueprint
import setting
import subscriptions
import objectpath
user_api = Blueprint('user_api', __name__)

@user_api.route('/user/<subscriptionId>/<principalId>')
def api_user_group(subscriptionId,principalId):
    userlist = []
    user_membership=get_user_membership(principalId)
    endpoint = setting.ROLE_ASSIGMENT_ENDPOINT % (subscriptionId,principalId)
    print(endpoint)
    headers  = {"Authorization": 'Bearer ' + autentication.get_token()}
    rolename= setting.ROLE_ASSIGMENT_NAME

    respond = requests.get(endpoint,headers=headers)
    status= respond.status_code
    print(status)
    if(status == 200):

        json_output = requests.get(endpoint,headers=headers).json()
        roles = json.loads(str(json_output).replace("'","\""))

        
        if rolename in str(json_output):
            roles_data = objectpath.Tree(roles['value'])
            proplist = tuple(roles_data.execute('$.properties'))
            for p in proplist:
                add_group=False
                role=p['roleDefinitionId']
                if (rolename in role)&(principalId == p['principalId']):
                    add_group=True
                else:
                    #add_group=check_group_member(p['principalId'],principalId)
                    if(p['principalId'] in user_membership):
                        add_group=True

                if(add_group):
                    rg=p['scope'].split('/').pop()
                    if(rg != subscriptionId):
                        userlist.append(rg)
                        print(userlist)
                
            return json.dumps(userlist)
        else:
            return "{}"  

    else:
        return "{}"    



@user_api.route('/user/subscriptions/<token>')
def api_user_subscriptions(token):
    
    endpoint = setting.SUBSCRIPTIONS_ENDPOINT
    headers = {"Authorization": 'Bearer ' + token}
    userlist = requests.get(endpoint,headers=headers).json()
    return (str(userlist))


def check_group_member(groupId,principalId):
    endpoint="https://graph.microsoft.com/v1.0/groups/"+groupId+"/members"
    print(endpoint)
    headers = {"Authorization": 'Bearer ' + autentication.get_token()}
    userlist = requests.get(endpoint,headers=headers).json()
    if(principalId in userlist):
        return True
    else:
        return False    


#@user_api.route('/user/subscriptions/membership/<principalId>')
def get_user_membership(principalId):
    try:
        endpoint="https://graph.microsoft.com/v1.0/users/"+principalId+"/memberOf"
        token=autentication.get_token_graph()
        print(token)
        headers = {"Authorization": 'Bearer ' + token}
        result = requests.get(endpoint,headers=headers).json()
        groups = [ sub['id'] for sub in result['value'] ] 
        print(groups)
        return str(groups)
    except:
        print("Error during process user memebership.. most likely permission")
        return ""

 

