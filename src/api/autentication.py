import os
import adal
from datetime import datetime
import requests
from azure.mgmt.compute import ComputeManagementClient
import azure.mgmt.resource
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.common.credentials import UserPassCredentials
from azure.mgmt.authorization import AuthorizationManagementClient
from msrestazure.azure_active_directory import MSIAuthentication
from azure.keyvault import KeyVaultClient, KeyVaultAuthentication
from dotenv import load_dotenv, find_dotenv
import setting


if "APPSETTING_WEBSITE_SITE_NAME" not in os.environ:
    load_dotenv(find_dotenv())
    # Development env
    TENANT_ID = os.getenv("TENANT_ID")
    CLIENT = os.getenv("CLIENT")
    KEY = os.getenv("KEY")
    SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")
    
    AUTHENTICATION_ENDPOINT = os.getenv("AUTHENTICATION_ENDPOINT")
    RESOURCE = os.getenv("RESOURCE")
    RESOURCE_KV = os.getenv("RESOURCE_KV")
    RESOURCE_GRAPH = os.getenv("RESOURCE_GRAPH")
    KEY_VAULT = os.getenv("KEY_VAULT")
    CLIENT_GRAPH = os.getenv("CLIENT_GRAPH")
    KEY_GRAPH= os.getenv("KEY_GRAPH")

def kv_get_secret(secret_id):
    client = KeyVaultClient(get_kv_credentials())
    value_id = client.get_secret(KEY_VAULT, secret_id, "")  
    if(value_id is None):
            return ("")
    else:
        print('Geting Secret %s with value %s' % (secret_id,value_id.value))
        return (value_id.value)
     
def  get_token():
     
     expiredtime=datetime.strptime(setting.TOKEN['expiresOn'],'%Y-%m-%d %H:%M:%S.%f')

     if( expiredtime < datetime.now()):
         print('expired token, init refesh token process')
         setting.TOKEN=get_token_init()
        
     return setting.TOKEN['accessToken']


def get_token_init():
    context = adal.AuthenticationContext(AUTHENTICATION_ENDPOINT + setting.TENANT_ID)
    token_response = context.acquire_token_with_client_credentials(RESOURCE, setting.CLIENT, setting.KEY)
    #print (token_response)
    return token_response

def get_token_graph():
    context = adal.AuthenticationContext(AUTHENTICATION_ENDPOINT + setting.TENANT_ID)
    token_response = context.acquire_token_with_client_credentials(RESOURCE_GRAPH, CLIENT_GRAPH, KEY_GRAPH)
    return token_response['accessToken']

def get_kv_credentials():
    
    if "APPSETTING_WEBSITE_SITE_NAME" in os.environ:
        return MSIAuthentication(
            resource=RESOURCE_KV
        )
    else:    

        credentials = ServicePrincipalCredentials(
        client_id = CLIENT,
        secret = KEY,
        tenant = TENANT_ID,
        resource = RESOURCE_KV
    )
    
    return credentials

