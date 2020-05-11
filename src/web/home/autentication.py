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
from  home import setting
import uuid

CLIENT = os.getenv("CLIENT")
CLIENT_ID = os.getenv("CLIENT_ID")
KEY = os.getenv("KEY")
SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")

TENANT_ID = os.getenv("TENANT_ID")
TENANT = os.getenv("TENANT")
AUTHENTICATION_ENDPOINT = os.getenv("AUTHENTICATION_ENDPOINT")
RESOURCE = os.getenv("RESOURCE")
RESOURCE_KV = os.getenv("RESOURCE_KV")
KEY_VAULT = os.getenv("KEY_VAULT")
RESOURCE_GRAPH = os.getenv("RESOURCE_GRAPH") 
AUTHORITY_HOST_URL = os.getenv("AUTHENTICATION_ENDPOINT")
API_VERSION = os.getenv("API_VERSION")
PORT = os.getenv("PORT")

AUTHORITY_URL = AUTHORITY_HOST_URL + '/' + TENANT
REDIRECT_URI = 'http://localhost:{}/getAToken'.format(PORT)
TEMPLATE_AUTHZ_URL = ('https://login.microsoftonline.com/{}/oauth2/authorize?' +
                      'response_type=code&client_id={}&redirect_uri={}&' +
                      'state={}&resource={}')
                      
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
         setting.TOKEN:get_token_init()
        
     return setting.TOKEN['accessToken']


def get_token_init():
    context = adal.AuthenticationContext(AUTHENTICATION_ENDPOINT + TENANT_ID)
    token_response = context.acquire_token_with_client_credentials(RESOURCE,CLIENT, KEY)
    print (token_response)
    return token_response

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

def get_ClientManagement():
    return ResourceManagementClient(get_credentials(), setting.SUBSCRIPTION_ID)


def get_client_Auth():
    return AuthorizationManagementClient(get_credentials(), setting.SUBSCRIPTION_ID)

def get_credentials():
    return ServicePrincipalCredentials(
        client_id = CLIENT,
        secret = KEY,
        tenant = TENANT_ID
    )



