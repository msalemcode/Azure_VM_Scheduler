import os
from home import setting

if "APPSETTING_WEBSITE_SITE_NAME" not in os.environ:
    CLIENT_ID = os.environ.get('CLIENT')
    CLIENT_SECRET = os.environ.get('KEY')
    TENANT_ID = os.environ.get('TENANT_ID')
    TENANT = os.environ.get('TENANT')
else:
    setting.load_kv_values()
    CLIENT_ID = setting.CLIENT
    CLIENT_SECRET = setting.KEY
    TENANT_ID = setting.TENANT_ID
    TENANT = setting.TENANT

print("TENANT %s" % TENANT)
print("TENANT ID %s" % TENANT_ID)



AUTH_CALLBACK_URL = 'account/signin/azure_ad/callback'

AUTHORIZE_ENDPOINT = 'https://login.microsoftonline.com/%s/oauth2/v2.0/authorize' % TENANT_ID
TOKEN_ENDPOINT = 'https://login.microsoftonline.com/%s/oauth2/v2.0/token/' % TENANT_ID
END_SESSION_ENDPOINT = 'https://login.microsoftonline.com/%s/oauth2/v2.0/logout' % TENANT_ID

RESOURCE = 'https://management.core.windows.net/'
GRAPH_RESOURCE = 'https://graph.microsoft.com/'
OUTLOOK_RESOURCE = 'https://outlook.office.com/'

SCOPES = [
    {
        'resource': GRAPH_RESOURCE,
        'permissions': [ 'User.Read' ]
    }
    
]