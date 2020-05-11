from .models import Group
import requests
import json
import datetime
from tzlocal import get_localzone
from ast import literal_eval
from datetime import datetime
from datetime import timedelta
import time
from dateutil import parser
from home import setting
from pytz import timezone
from .subscriptions import get_resourcegroup_vmlist, get_resourcegroup_vmstatus


def get_groups(request):
    endpoint=setting.REST_API_ENDPOINT+'/user/'+setting.SUBSCRIPTION_ID+'/'+str(request.session['principlid'])
    print(endpoint)
    mygroup=requests.get(endpoint).json()
    print(mygroup)
    return mygroup

def get_currentuser_groups(request):
    
    print("get_currentuser_groups")
    print(setting.SUBSCRIPTION_ID)
    print(setting.REST_API_ENDPOINT)

    usergroup=requests.get(setting.REST_API_ENDPOINT+'/user/'+setting.SUBSCRIPTION_ID+'/'+str(request.session['principlid'])).json()
    runbook_start_schedules=get_runbook_schedules_list(setting.RUNBOOK_START)
    runbook_shutdown_schedules=get_runbook_schedules_list(setting.RUNBOOK_STOP)
    print("========================= User Groups ========================================")
    print(usergroup)
    print("========================= Start Schedule ========================================")
    print(runbook_start_schedules)
    print("========================= Stop Schedul ========================================")
    print(runbook_shutdown_schedules)
    
    mygroup= []
    setting.INDEX=-1
    for item in usergroup:
        newItem=True
        for g in mygroup:
            if (g.group_name == item):
                newItem=False
            
        if (item not in setting.IGNORE_GROUPS) & newItem:
            check_group_schedule(item,mygroup,runbook_start_schedules,runbook_shutdown_schedules)
    #print("========================= print groups ========================================")      

    check_if_all_user_group_added(usergroup,mygroup)
    for group in mygroup:       
        request.session['group_'+str(group.id)]= [group.id,group.group_name,group.group_schid,group.group_desc,group.start_time,group.shutdown_time,group.schedule_end,group.vm_list,group.recurring,group.time_zone]
    request.session['maxgroupnum']=setting.INDEX+1  
    setting.RESOURCE_GROUPS=usergroup 
    return mygroup

def check_if_all_user_group_added(usergroup,mygroup):
    for item in usergroup:
        print("Check now if Item %s added",item)
        found=False
        for g in mygroup:
            if(g.group_name==item):
                found=True
                break
        if (not found):
            setting.INDEX=setting.INDEX+1
            print("adding Blank group")
            mygroup.append(Group(setting.INDEX,item,"","","","","","","","")) 


#utilites functions
def check_group_schedule1(item,mygroup,i,startlist,stoplist):
    newItem=True

    for g in mygroup:
        if (g.group_name == item):
            newItem=False
            break

    if(newItem):
    # Check if schedule exists 
        schedule_start= setting.SUBSCRIPTION_ID+"_"+item+"_start"
        schedule_stop= setting.SUBSCRIPTION_ID+"_"+item+"_stop"
        start_time=None
        schedule_end=None
        recurring=None
        time_zone="UTC"
        print ("Check if schedule exists for item %s for following schedules" % item)
        print(schedule_start)
        print(schedule_end)
        print("======================================================================")
        for x in startlist:
            
            print("process Start linked schedule ----->")
            print(x["name"])
            print("<-----")
            if (x["name"]==schedule_start):

                start_time=format_str_date((x["startTime"][:16]).replace("T"," ").replace("-","/"))
                recurring =x["scheduleType"]
                if( recurring==1):
                    schedule_end=format_str_date((x['recurrenceSetting']["expiryTime"][:16]).replace("T"," ").replace("-","/"))
                    recurring='on'
                time_zone=x["timeZone"]
                break
        stop_time=None  
        
        for x in stoplist:
            print("process Stop linked schedule ----->")
            print(x["name"])
            print("<-----")
            if (x["name"]==schedule_stop):
                stop_time=format_str_date((x["startTime"][:16]).replace("T"," ").replace("-","/"))
                recurring =x["scheduleType"]
                if( recurring==1):
                   # stop_time_end=format_str_date((x['recurrenceSetting']["expiryTime"][:16]).replace("T"," ").replace("-","/"))
                    recurring='on'
                break
        
        vmlist=check_runbook_schedule_link(schedule_start,setting.RUNBOOK_START)
        print("add the group")
        mygroup.append(Group(i,item,start_time,stop_time,schedule_end,vmlist,recurring,time_zone))


#utilites functions
def check_group_schedule(item,mygroup,startlist,stoplist):

    # Check if schedule exists 
        schedule_start= item+"_start"
        schedule_stop= item+"_stop"
        start_time=None
        stop_time=None
        schedule_end=None
        recurring=None
        time_zone="UTC"
        print ("Check if schedule exists for item %s" % item)
        print(schedule_start)
        found=0
        for x in startlist:
            print("process start linked schedule ----->")
            print(x["name"])
            print("<-----")
            if (schedule_start in x["name"]):

                start_time=format_str_date((x["startTime"][:16]).replace("T"," ").replace("-","/"))
                recurring =x["scheduleType"]
                if( recurring==1):
                    schedule_end=format_str_date((x['recurrenceSetting']["expiryTime"][:16]).replace("T"," ").replace("-","/"))
                    recurring='on'
                time_zone=x["timeZone"]
                  
                for y in stoplist:
                    print("process stop linked schedule ----->")
                    print(x["name"])
                    print("<-----")
                    if (x["name"]==y["name"].replace("stop","start")):
                        stop_time=format_str_date((y["startTime"][:16]).replace("T"," ").replace("-","/"))
                        #break
        
                vmlist=check_runbook_schedule_link(x["name"],setting.RUNBOOK_START)
                print("======== adding group now ==============================")
                print(item)
                print(start_time)
                print(stop_time)
                print(schedule_end)
                print(vmlist)
                print(recurring)
                print(time_zone)
                print("========================================================")
                setting.INDEX=setting.INDEX+1
                group_schid=x["name"].replace("_start","")
                group_desc=x["description"]
                print("adding group")
                 #group_name,group_schid,group_desc,start_time,shutdown_time,schedule_end,vm_list,recurring,time_zone,
                mygroup.append(Group(setting.INDEX,item,group_schid,group_desc,start_time,stop_time,schedule_end,vmlist,recurring,time_zone))
                found=1
# we need to check if there is shutdown schedule without start, we add the logic after adding sched desc name

        if(found==0):
            print("could not found schedule based on Start Schedule.. Test again")
            for x in stoplist:
                print("process stop linked schedule ----->")
                print(x["name"])
                print("<-----")
                if (schedule_stop in x["name"]):
                    start_time=format_str_date((x["startTime"][:16]).replace("T"," ").replace("-","/"))
                    recurring =x["scheduleType"]
                    if( recurring==1):
                        schedule_end=format_str_date((x['recurrenceSetting']["expiryTime"][:16]).replace("T"," ").replace("-","/"))
                        recurring='on'
                    time_zone=x["timeZone"]
                    start_time=None 
                    vmlist=check_runbook_schedule_link(x["name"],setting.RUNBOOK_START)
                    print("======== adding group now ==============================")
                    print(item)
                    print(start_time)
                    print(stop_time)
                    print(schedule_end)
                    print(vmlist)
                    print(recurring)
                    print(time_zone)
                    print("========================================================")
                    setting.INDEX=setting.INDEX+1
                    group_schid=x["name"].replace("_start","")
                    group_desc=x["description"]
                    print("adding group")
                    mygroup.append(Group(setting.INDEX,item,group_schid,group_desc,start_time,stop_time,schedule_end,vmlist,recurring,time_zone)) 

def get_runbook_schedules_list(runbooktype):
    try:

         link_api_url =  setting.REST_API_ENDPOINT+'/runbookslinked/'+setting.AUTO_SUBSCRIPTION_ID+'/'+setting.AUTOMATION_GROUP +'/'+setting.AUTOMATION_ACCOUNT+'/'+runbooktype
         print(link_api_url)
         rest = requests.get(link_api_url).text
         result=literal_eval(rest)  
         print(result)
         return result 
    except Exception as e: 
        print("Error during process the request: %s" % e)
    return []

def check_schedule_exists(schid):
    try:
        sch_api_url =  setting.REST_API_ENDPOINT+'/schedules/'+setting.AUTO_SUBSCRIPTION_ID+'/'+setting.AUTOMATION_GROUP +'/'+setting.AUTOMATION_ACCOUNT+'/'+schid
        print(sch_api_url)

        result = requests.get(sch_api_url).content.decode('utf8').replace("'", '"')
        if "Not Found" not in result:
            result_dict =literal_eval(result)    
            run_time = result_dict["properties"]["startTime"]
        
            if run_time != None:
                run_time= utc_to_local(run_time)
                print("schedule run time for schedule %s is " % schid, run_time)
                return run_time
    except Exception as e: 
        print("Error during process the request: %s" % e)
    return None


def check_runbook_schedule_link(schid,runbookid):
    try:
        print("get link schedule detail")
        print(schid)
        print(runbookid)
        sch_api_url =  setting.REST_API_ENDPOINT+'/runbooks/'+setting.AUTO_SUBSCRIPTION_ID+'/'+setting.AUTOMATION_GROUP +'/'+setting.AUTOMATION_ACCOUNT+'/'+runbookid+'/'+schid
        print(sch_api_url)
        result = (requests.get(sch_api_url).content.decode('utf8').replace("'", '"')).replace('""', '"')
        if(result !=None):
            print(result)
            vmlist=(json.loads(result))[2]
            print(vmlist["value"])
            return vmlist["value"].split(",")
        else:
             return ""


    except Exception as e: 
        print("Error during process the request: %s" % e)
    return ""


def update_group_schedule(group):
    print("start update or add new schedule")
    print(group)
    #group_name,group_schid,group_desc,start_time,shutdown_time,schedule_end,vm_list,recurring,time_zone,
    schedule_start= group.group_schid+"_start"
    schedule_stop= group.group_schid+"_stop"

    print(group.recurring)
    print("new_start_time ->" +group.start_time)
    print("new_shutdown_time ->" +group.shutdown_time)
   
    if group.start_time!=None :
        update_schedule_time(schedule_start,group.group_desc,group.start_time,group.schedule_end,group.vm_list,group.recurring,group.time_zone)
        Create_schedule_link(setting.RUNBOOK_START,schedule_start,group.group_name,group.vm_list)

    if group.shutdown_time != None:
        update_schedule_time(schedule_stop,group.group_desc,group.shutdown_time,group.schedule_end,group.vm_list,group.recurring,group.time_zone)
        Create_schedule_link(setting.RUNBOOK_STOP,schedule_stop,group.group_name,group.vm_list)


def update_schedule_time(schid,desc,newtime,endtime,vm_list,recurring,timezone):
    try:
        #('/schedules/<subid>/<groupid>/<automationid>/<schid>', methods=['PUT'])
        todaydate= format_date_time2(newtime)+timezone_diff(timezone)
        print(todaydate)
        expiredate = format_date_time2(endtime)+timezone_diff(timezone)
        print(expiredate)
        sch_api_url =  setting.REST_API_ENDPOINT+'/schedules/'+setting.AUTO_SUBSCRIPTION_ID+'/'+setting.AUTOMATION_GROUP +'/'+setting.AUTOMATION_ACCOUNT+'/'+ schid
        print(sch_api_url)
        if(recurring=='1')or(recurring=='on'):
            obj = {
                    "name": schid,
                    "properties": {
                        "description": desc,
                        "startTime": todaydate,
                        "expiryTime": expiredate,
                        "interval": 1,
                        "frequency": "Day", 
                        "timezone" :timezone
                }
            }
        else:
            obj = {
                "name": schid,
                "properties": {
                    "description": desc,
                    "startTime": todaydate,
                    "expiryTime": todaydate,
                    "interval": None,
                    "frequency":"OneTime",
                    "timezone" :timezone
                }
            }



        print(obj)
        headers = {"Content-type": "application/json"}

        print(sch_api_url)
        result = requests.put(sch_api_url,data=json.dumps(obj),headers=headers).content.decode('utf8').replace("'", '"')
        print("Return result for update schedule --->")
        print(result)
    except Exception as e: 
        print("Error during process the request: %s" % e)
    return False    


def Create_schedule_link(runbooks,schid,rg,vmlist):
    #@runbooks_api.route('/runbooks/<subid>/<groupid>/<automationid>/<rubbookid>/<schid>', methods=['POST'])      
    print('update link schedule')
    try:
        data =[
                    {"name":"ResourceGroupName"  ,"value":"\""+rg+"\""},
                    {"name":"AzureSubscriptionID","value":"\""+setting.SUBSCRIPTION_ID+"\""},
                    {"name":"VMList","value":"\""+vmlist+"\""},
                ]
        print(data)
        link_api_url =  setting.REST_API_ENDPOINT+'/runbooks/'+setting.AUTO_SUBSCRIPTION_ID+'/'+setting.AUTOMATION_GROUP +'/'+setting.AUTOMATION_ACCOUNT+'/'+runbooks+'/'+ schid
        headers = {"Content-type": "application/json"}
        print(link_api_url)
        result = requests.post(link_api_url,data=json.dumps(data),headers=headers).content.decode('utf8').replace("'", '"')
        print(result)
    except Exception as e: 
            ("Error during process the request: %s" % e)
      

def delete_group_schedule(group):
    try:
        #get variables from group
        sch= group.group_schid
        schedule_start= sch+"_start"
        schedule_stop= sch+"_stop"


        print(schedule_start)
        print(schedule_stop)

        # delete the start schedule
        api_url =  setting.REST_API_ENDPOINT+'/schedules/'+setting.AUTO_SUBSCRIPTION_ID+'/'+setting.AUTOMATION_GROUP +'/'+setting.AUTOMATION_ACCOUNT+'/'+ schedule_start
        print(api_url)
        requests.delete(api_url)

        # delete the stop schedule
        api_url =  setting.REST_API_ENDPOINT+'/schedules/'+setting.AUTO_SUBSCRIPTION_ID+'/'+setting.AUTOMATION_GROUP +'/'+setting.AUTOMATION_ACCOUNT+'/'+ schedule_stop
        print(api_url)
        requests.delete(api_url)
        return True
    except Exception as e: 
        ("Error during process the request: %s" % e)
        return False

    
def format_date_time(nday):
    
    newdate= (datetime.today() + timedelta(days=nday)).strftime('%Y-%m-%d')+"T"+"00:00:00"
    return newdate


def format_date_time2(newtime):
    #10/23/2019 13:50
    year=newtime[6]+newtime[7]+newtime[8]+newtime[9]
    day=newtime[3]+newtime[4]
    month=newtime[0]+newtime[1]
    newdate=year+"-"+month+"-"+day+"T"+newtime[11:]
    return newdate    

def format_str_date(newtime):
    print("newtime ->"+newtime)
    year=newtime[:4]
    month=newtime[5]+newtime[6]
    day=newtime[8]+newtime[9]
    newdate=month+"/"+day+"/"+year+" "+newtime[11:]
    print(newdate)

    return newdate

def utc_to_local(utc_datetime):
    print(utc_datetime)
    todaydate = parser.parse(utc_datetime)
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    print(offset)
    localtime = todaydate-offset
    return str(localtime.time()) 


def timezone_diff(argument):
    tz = timezone(argument)
    offset=int(((tz.utcoffset(datetime.utcnow()).seconds)/3600)-24)
    #print(offset)
    delta=str(offset)+":00"
    return delta    
