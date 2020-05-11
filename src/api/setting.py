import autentication

AUTOMATION_ENDPOINT = ""
SUBSCRIPTIONS_ENDPOINT = ""
RESOURCEGROUPS_ENDPOINT = ""
RESOURCEGROUP_ENDPOINT = ""
RUNBOOKS_ENDPOINT = ""
RUNBOOK_ENDPOINT = ""
RUNBOOK_SCHEDULE_ENDPOINT = ""
RUNBOOK_CONTENT_ENDPOINT = ""
RUNBOOK_PARAMETER_ENDPOINT = ""
SCHEDULE_PARAMETER_ENDPOINT = ""
RUNBOOK_SCHEDULE_PARAMETERS_ENDPOINT = ""
RUNBOOK_SCHEDULES_LIST_ENDPOINT = ""
SCHEDULE_ENDPOINT =""
SCHEDULES_ENDPOINT =""
JOBS_ENDPOINT = ""
JOB_ENDPOINT = ""
JOB_CONTROL_ENDPOINT = ""
JOB_SCHEDULES_ENDPOINT = ""
JOB_SCHEDULE_ENDPOINT = ""
SUBSCRIPTION_ID = ""
TENANT_ID = ""
CLIENT = ""
KEY = ""
TOKEN =""
ROLE_ASSIGMENT_ENDPOINT=""
ROLE_ASSIGMENT_NAME=""
RESOURCEGROUP_VMS_ENDPOINT=""
RUNBOOK_SCHEDULE_DELETE_ENDPOINT=""

RESOURCEGROUP_VM_STATUS_ENDPOINT=""

RESOURCEGROUP_VM_START_ENDPOINT =""
RESOURCEGROUP_VM_STOP_ENDPOINT=""
RESOURCEGROUP_VM_RESTART_ENDPOINT=""

def load_kv_values():
    global AUTOMATION_ENDPOINT
    AUTOMATION_ENDPOINT = autentication.kv_get_secret("automation-endpoint").rstrip()

    global SUBSCRIPTIONS_ENDPOINT
    SUBSCRIPTIONS_ENDPOINT = autentication.kv_get_secret("subscriptions-endpoint").rstrip()

    global RESOURCEGROUPS_ENDPOINT
    RESOURCEGROUPS_ENDPOINT = autentication.kv_get_secret("resourcegroups-endpoint").rstrip()
    
    global RESOURCEGROUP_ENDPOINT
    RESOURCEGROUP_ENDPOINT = autentication.kv_get_secret("resourcegroup-endpoint").rstrip()

    global RUNBOOKS_ENDPOINT
    RUNBOOKS_ENDPOINT = autentication.kv_get_secret("runbooks-endpoint").rstrip()

    global RUNBOOK_ENDPOINT
    RUNBOOK_ENDPOINT = autentication.kv_get_secret("runbook-endpoint").rstrip()

    global RUNBOOK_CONTENT_ENDPOINT
    RUNBOOK_CONTENT_ENDPOINT = autentication.kv_get_secret("runbook-content-endpoint").rstrip()

    global RUNBOOK_PARAMETER_ENDPOINT
    RUNBOOK_PARAMETER_ENDPOINT =  autentication.kv_get_secret("runbook-parameter-endpoint").rstrip()


    global RUNBOOK_SCHEDULE_PARAMETERS_ENDPOINT 
    RUNBOOK_SCHEDULE_PARAMETERS_ENDPOINT  =  autentication.kv_get_secret("runbook-schedule-parameters-endpoint").rstrip()

    global SCHEDULE_PARAMETER_ENDPOINT 
    SCHEDULE_PARAMETER_ENDPOINT  = autentication.kv_get_secret("schedule-parameter-endpoint").rstrip()

    global SCHEDULE_ENDPOINT 
    SCHEDULE_ENDPOINT  = autentication.kv_get_secret("schedule-endpoint").rstrip()

    global SCHEDULES_ENDPOINT
    SCHEDULES_ENDPOINT = autentication.kv_get_secret("schedules-endpoint").rstrip()

    global RUNBOOK_SCHEDULE_ENDPOINT
    RUNBOOK_SCHEDULE_ENDPOINT = autentication.kv_get_secret("runbook-schedule-endpoint").rstrip()

    global JOBS_ENDPOINT
    JOBS_ENDPOINT = autentication.kv_get_secret("jobs-endpoint").rstrip()

    global JOB_ENDPOINT
    JOB_ENDPOINT = autentication.kv_get_secret("job-endpoint").rstrip()

    global JOB_CONTROL_ENDPOINT
    JOB_CONTROL_ENDPOINT = autentication.kv_get_secret("job-control-endpoint").rstrip()

    global JOB_SCHEDULES_ENDPOINT
    JOB_SCHEDULES_ENDPOINT = autentication.kv_get_secret("job-schedules-endpoint").rstrip()

    global JOB_SCHEDULE_ENDPOINT
    JOB_SCHEDULE_ENDPOINT = autentication.kv_get_secret("job-schedule-endpoint").rstrip()

    global SUBSCRIPTION_ID
    SUBSCRIPTION_ID = autentication.kv_get_secret("subscriptionid")

    global TENANT_ID
    TENANT_ID = autentication.kv_get_secret("tenantid")

    global CLIENT
    CLIENT =  autentication.kv_get_secret("client")

    global KEY
    KEY = autentication.kv_get_secret("key")

    global TOKEN
    TOKEN = autentication.get_token_init()

    global RUNBOOK_SCHEDULES_LIST_ENDPOINT
    RUNBOOK_SCHEDULES_LIST_ENDPOINT= autentication.kv_get_secret("runbook-schedules-list-endpoint").rstrip()

    global ROLE_ASSIGMENT_ENDPOINT
    ROLE_ASSIGMENT_ENDPOINT=autentication.kv_get_secret("role-assignment-endpoint").rstrip()
    
    global ROLE_ASSIGMENT_NAME
    ROLE_ASSIGMENT_NAME=autentication.kv_get_secret("role-assignment-name").rstrip()    

    global RESOURCEGROUP_VMS_ENDPOINT
    RESOURCEGROUP_VMS_ENDPOINT=autentication.kv_get_secret("resourcegroup-vmlist-endpoint").rstrip()  
    #RESOURCEGROUP_VMS_ENDPOINT="https://management.azure.com/subscriptions/%s/resourcegroups/%s/providers/Microsoft.Compute/virtualMachines?api-version=2019-03-01"   

    global RUNBOOK_SCHEDULE_DELETE_ENDPOINT
    RUNBOOK_SCHEDULE_DELETE_ENDPOINT=autentication.kv_get_secret("runbook-schedule-delete-endpoint").rstrip()  
    #RUNBOOK_SCHEDULE_DELETE_ENDPOINT="https://s2.automation.ext.azure.com/api/Orchestrator/UnlinkRunbookFromSchedule?runbookId=%s&scheduleId=%s"

    global RESOURCEGROUP_VM_STATUS_ENDPOINT
    RESOURCEGROUP_VM_STATUS_ENDPOINT=autentication.kv_get_secret("resourcegroup-vm-status-endpoint").rstrip()  
    #RESOURCEGROUP_VM_STATUS_ENDPOINT="https://management.azure.com/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Compute/virtualMachines/%s?$expand=instanceView&api-version=2019-03-01"

    global RESOURCEGROUP_VM_START_ENDPOINT
    RESOURCEGROUP_VM_START_ENDPOINT=autentication.kv_get_secret("resourcegroup-vm-start-endpoint").rstrip() 
    #RESOURCEGROUP_VM_START_ENDPOINT="https://management.azure.com/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Compute/virtualMachines/%s/start?api-version=2019-03-01"

    global RESOURCEGROUP_VM_STOP_ENDPOINT
    RESOURCEGROUP_VM_STOP_ENDPOINT=autentication.kv_get_secret("resourcegroup-vm-stop-endpoint").rstrip() 
    #RESOURCEGROUP_VM_STOP_ENDPOINT="https://management.azure.com/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Compute/virtualMachines/%s/powerOff?api-version=2019-03-01"

    global RESOURCEGROUP_VM_RESTART_ENDPOINT
    RESOURCEGROUP_VM_RESTART_ENDPOINT=autentication.kv_get_secret("resourcegroup-vm-restart-endpoint").rstrip() 
    #RESOURCEGROUP_VM_RESTART_ENDPOINT="https://management.azure.com/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Compute/virtualMachines/%s/restart?api-version=2019-03-01"

