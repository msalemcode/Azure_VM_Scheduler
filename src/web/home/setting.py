
from  home import autentication

SUBSCRIPTION_ID = ""
AUTO_SUBSCRIPTION_ID = ""
TENANT_ID = ""
TENANT = ""

CLIENT = ""
KEY = ""
REST_API_ENDPOINT =""
RUNBOOK_START = ""
RUNBOOK_STOP = ""
AUTOMATION_ACCOUNT =""
IGNORE_GROUPS = ""
AUTOMATION_GROUP= ""
RESOURCE_GROUP=""
RESOURCE_GROUPS=""
SCHEDULE_ID=""
NEWLINE=""
CURRENT_RESOURCE_GROUP=""


def set_current_resouce_group(gid):
    global CURRENT_RESOURCE_GROUP
    CURRENT_RESOURCE_GROUP=gid

def set_current_subscription(sid):
    global SUBSCRIPTION_ID
    SUBSCRIPTION_ID=sid


def load_kv_values():

    global TENANT_ID
    TENANT_ID = autentication.kv_get_secret("tenantid")
    
    global TENANT
    TENANT = autentication.kv_get_secret("tenant")

    global CLIENT
    CLIENT =  autentication.kv_get_secret("web-client-id")

    global KEY
    KEY = autentication.kv_get_secret("web-client-key")

    global REST_API_ENDPOINT
    REST_API_ENDPOINT = autentication.kv_get_secret("rest-api-endpoint")
    #REST_API_ENDPOINT ="http://localhost:5000"

    global RUNBOOK_START
    RUNBOOK_START = autentication.kv_get_secret("runbook-start")

    global RUNBOOK_STOP
    RUNBOOK_STOP = autentication.kv_get_secret("runbook-stop")

    global AUTOMATION_ACCOUNT
    AUTOMATION_ACCOUNT =autentication.kv_get_secret("automation-account")

    global IGNORE_GROUPS
    IGNORE_GROUPS = autentication.kv_get_secret("ignore-groups")

    global AUTOMATION_GROUP
    AUTOMATION_GROUP= autentication.kv_get_secret("automation-group")

    global AUTO_SUBSCRIPTION_ID
    AUTO_SUBSCRIPTION_ID= autentication.kv_get_secret("subscriptionid")

  

  

    