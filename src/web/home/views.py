from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse,HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
import json
from django.contrib.sessions.backends.db import SessionStore
from azure.mgmt.resource import ResourceManagementClient, SubscriptionClient
import requests
from django.views.generic import TemplateView
from .models import Group
from .models import Subscription,VM_STATUS,GROUP_DD
from .forms import GroupForm
from django.core import serializers
from account import auth, token_cache, settings as auth_settings
from account.graph_service import GraphService
from home import autentication , setting, schedules
from .subscriptions import list_subscriptions, get_valid_subscription,get_resourcegroup_vmlist,get_resourcegroup_vmstatus,post_vm_action
from datetime import datetime
import uuid
import time

@login_required
def group_list(request):
    
    if(setting.SUBSCRIPTION_ID is ""):
        return HttpResponseRedirect('/')

    # call the REST API and get User Group
    if not request.session:
        request.session={}

    print('subscripoint is '+setting.SUBSCRIPTION_ID)
    print('current user Id is '+ request.session['principlid'])
    mygroup = schedules.get_currentuser_groups(request)    
    return render(request, 'home/group_list.html', {'groups': mygroup})


@login_required
def save_add_group_form(request,form, template_name):
    print("Start adding form")
    data = dict()
    data['schedule']=False
    if request.method == 'POST':
        print("it is post")
        if form.is_valid():
            print("form is valid")
            data['form_is_valid'] = True
            data['schedule']=True
            # get schedule group variable
            print('update session with updated group')
            vmselectlist = request.POST.getlist('vm_list')
            print('selected vm  --->')
            print(vmselectlist)
            #modify variables
            recurring=''
            if request.POST['recurring']=='1':
                recurring='on'
            groupvm=",".join(vmselectlist)

            x=form.instance.pk
            if (setting.NEWLINE=="1"):
                x=request.session['maxgroupnum'] 
                request.session['maxgroupnum']=x+1 
            #update the schedule
            print("=============================================")
            print("PK for new added sch ---->" + str(x))
            print("current session pk ---->" + str(form.instance.pk))
            print("=============================================")
            group=Group(x,request.POST["group_name"], 
                                                            form.instance.group_schid,
                                                            request.POST["group_desc"],
                                                            request.POST['start_time'],
                                                            request.POST['shutdown_time'],
                                                            request.POST['schedule_end'],
                                                            groupvm,
                                                            recurring,
                                                            request.POST['time_zone'])    
            schedules.update_group_schedule(group)
            request.session['group_'+str(x)] =[x,request.POST["group_name"], 
                                                            form.instance.group_schid,
                                                            request.POST["group_desc"],
                                                            request.POST['start_time'],
                                                            request.POST['shutdown_time'],
                                                            request.POST['schedule_end'],
                                                            vmselectlist,
                                                            recurring,
                                                            request.POST['time_zone']]

            print('get new group list from session')
            groups = get_groups_from_session (request)
            setting.NEWLINE="0"
            data['html_group_list'] = render_to_string('home/includes/partial_group_list.html', {
                'groups': groups
            })
        else:
            print("not vaid")
            data['form_is_valid'] = False
    
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)

    return JsonResponse(data)

@login_required
def save_update_group_form(request,form, template_name):
    print("Start Saving form")
   
    data = dict()
    data['schedule']=False
    if request.method == 'POST':
        print("it is post")
        
        if form.is_valid():
            print("form is valid")
            data['form_is_valid'] = True
            data['schedule']=True
            # get schedule group variable
            print('update session with updated group')
            vmselectlist = request.POST.getlist('vm_list')
            
            print('selected vm  --->')
            print(vmselectlist)
            #modify variables
            recurring=''
            if request.POST['recurring']=='1':
                recurring='on'

            groupvm=",".join(vmselectlist)
            #update the schedule
            group=Group(form.instance.pk,request.POST["group_name"], 
                                                            form.instance.group_schid,
                                                            request.POST["group_desc"],
                                                            request.POST['start_time'],
                                                            request.POST['shutdown_time'],
                                                            request.POST['schedule_end'],
                                                            groupvm,
                                                            recurring,
                                                            request.POST['time_zone'])    
            schedules.update_group_schedule(group)


            request.session['group_'+str(form.instance.pk)] =[form.instance.pk,request.POST["group_name"], 
                                                            form.instance.group_schid,
                                                            request.POST["group_desc"],
                                                            request.POST['start_time'],
                                                            request.POST['shutdown_time'],
                                                            request.POST['schedule_end'],
                                                            vmselectlist,
                                                            recurring,
                                                            request.POST['time_zone']]

            print(request.session['group_'+str(form.instance.pk)]) 

            print('get new group list from session')
            groups = get_groups_from_session (request)
            
            data['html_group_list'] = render_to_string('home/includes/partial_group_list.html', {
                'groups': groups
            })
        else:
            print("not vaid")
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def group_create(request,pk):
    print('hello')
 
    if request.method == 'POST':
        sch_id=setting.SUBSCRIPTION_ID+"_"+str(uuid.uuid1())+"_"+request.POST["group_name"]

        group=Group(pk,request.POST["group_name"],sch_id,request.POST["group_desc"],request.POST['start_time'],request.POST['shutdown_time'],request.POST['schedule_end'],request.POST['vm_list'],request.POST['recurring'],request.POST['time_zone'])
        form = GroupForm(request.POST, instance=group)
    else:
        print("Not POST")
        x = request.session['maxgroupnum']  
        editline= request.session['group_'+str(pk)]

        if(editline[4]=='' and editline[5]=='' and editline[6]==''):
            setting.NEWLINE="0"
            x=pk
        else:
            setting.NEWLINE="1"
        print("================= New Line to Add=========================")
        print(editline)
        print("PK ---->"+str(x))
        print("==========================================================")

        setting.RESOURCE_GROUP= editline[1]
        group=Group(x,editline[1],'','','','','','','','')
        #group=Group(editline[0],editline[1],editline[2],editline[3],editline[4],['magdydelete4','magdydeletevm'],rec,editline[7])
        form = GroupForm(instance=group)
    return save_add_group_form(request, form, 'home/includes/partial_group_create.html')

@login_required
def group_update(request,pk):
    print("begin Update PK")
    group=None
    
    if request.method == 'POST':
        print("POST NOW")
        editline= request.session['group_'+str(pk)]
        print(editline)
        if(editline[2]==""):
            schid=setting.SUBSCRIPTION_ID+"_"+str(uuid.uuid1())+"_"+request.POST["group_name"]
        else:
            schid=editline[2]

        group=Group(pk,request.POST["group_name"],schid,request.POST["group_desc"],request.POST['start_time'],request.POST['shutdown_time'],request.POST['schedule_end'],request.POST['vm_list'],request.POST['recurring'],request.POST['time_zone'])
        form = GroupForm(request.POST, instance=group)
    else:
        print("Not POST")
        editline= request.session['group_'+str(pk)]
        print(editline)
        recurring='0'
        if editline[8]=='on':
            recurring='1'
        setting.RESOURCE_GROUP= editline[1]
        group=Group(editline[0],editline[1],editline[2],editline[3],editline[4],editline[5],editline[6],editline[7],recurring,editline[9])
        #group=Group(editline[0],editline[1],editline[2],editline[3],editline[4],['magdydelete4','magdydeletevm'],rec,editline[7])
        form = GroupForm(instance=group)
    return save_update_group_form(request, form, 'home/includes/partial_group_update.html')


@login_required
def group_delete(request, pk):
    print("begin delete PK")
    data = dict()
    data['schedule']=False
    editline= request.session['group_'+str(pk)]
    group=Group(editline[0],editline[1],editline[2],editline[3],editline[4],editline[5],editline[6],editline[7],editline[8],editline[9])
    if request.method == 'POST':
        print("POST NOW")
        print("PK--->"+ str(pk))
        data['form_is_valid'] = schedules.delete_group_schedule(group)
        data['schedule']=True
        #check if the RG exist with other schedule
        x=request.session['maxgroupnum']          
        idx=0
        for i in range(0,x):
            key='group_'+str(i)
            if key in request.session:
                print("Key Exist-->"+key)
                editline= request.session[key] 
                if(editline[1]==group.group_name):
                     idx=idx+1
       
        print("Index for -->"+str(idx))
        if(idx==1):
            print("add group as blank")
            request.session['group_'+str(pk)] =  [pk,group.group_name,"","","","","","","",""]
        else:
            print("remove group from session")
            del request.session['group_'+str(pk)]
            request.session.modifed=True

        groups = get_groups_from_session (request)
        #groups = schedules.get_get_currentuser_groups(request)
        data['html_group_list'] = render_to_string('home/includes/partial_group_list.html', {
                'groups': groups
        })
        
    else:
        print("Not POST")
        context = {'group': group}
        data['html_form'] = render_to_string('home/includes/partial_group_delete.html', context, request=request)
    return JsonResponse(data)
    
@login_required
def get_groups_from_session (request):
    groups=[]
    x=request.session['maxgroupnum']          
    print('maxgroupnum = ' +str(x))
    for i in range(0,x):
        editline= request.session.get('group_'+str(i))
        if(editline != None):
            print("line item #")
            print(editline)
            recurring=editline[8]
            if(editline[8]=='1'):
                recurring='on'
            groups.append(Group(editline[0],editline[1],editline[2],editline[3],editline[4],editline[5],editline[6],editline[7],recurring,editline[9]))
    return groups


@login_required
def index(request):  
    if(setting.REST_API_ENDPOINT is ""):
        setting.load_kv_values()

    print("************ loading index pg")

    graph_access_token = auth.get_access_token(request, auth_settings.GRAPH_RESOURCE)
    graph_service = GraphService(graph_access_token)
    userprofile = json.loads(str(graph_service.get_me()).replace("'","\"").replace("None","\"\""))
    print("User Princile ID # " + userprofile['id'])
    request.session['principlid']= userprofile['id']
    
    #user_token = auth.get_access_token(request, autentication.RESOURCE)
    #print("Local time is "+ request.get('time'))
    mysubscriptions = list_subscriptions()     
    sublist = get_valid_subscription(requests,mysubscriptions,userprofile['id'])

    context = {'subscriptions': sublist}   
    
    return render(request,'home/index.html', context)

@login_required
def get_detail(request): 
    print("get resouce groups list")
    mygroup = schedules.get_groups(request)
    groups=[]
    for g in mygroup:
        if g==setting.CURRENT_RESOURCE_GROUP:
            groups.append(GROUP_DD(g,g,'selected'))
        else:
            groups.append(GROUP_DD(g,g,'false'))

    #request.session["current_resouce_group"]=groups
    vms=[] 
    context = {'groups': groups,'vmslist':vms}   
    return render(request,'home/detail.html', context)

@login_required
def user_groups(request):   
    print ("hello from main page post")
    sub_name = request.POST['dropdownl']
    setting.set_current_subscription(sub_name)
    request.session['current_sub']=sub_name
    print(setting.SUBSCRIPTION_ID)
    if ('schedule' in request.POST):
        print('this is schedule')
        return HttpResponseRedirect('groups')     

    if ('detail' in request.POST):
        print('this is detail')
        return HttpResponseRedirect('detail')   

@login_required
def getvmlist(request):

    print ("hello from detail page post")
    group_name = request.POST['dropdownl']
    setting.set_current_resouce_group(group_name)
    setting.SUBSCRIPTION_ID=request.session['current_sub']
    print("current sub -->"+setting.SUBSCRIPTION_ID)
    print("current rg -->"+setting.CURRENT_RESOURCE_GROUP)
    vms=get_resourcegroup_vmstatus()
    vmslist=[]
    for vm in vms:
        vmslist.append(VM_STATUS(vm['vm_name'],vm['vm_name'],vm['status'].upper()))
    mygroup = schedules.get_groups(request)
    #mygroup=request.session["current_resouce_group"]
    groups=[]
    for g in mygroup:
        if g==setting.CURRENT_RESOURCE_GROUP:
            groups.append(GROUP_DD(g,g,'selected'))
        else:
            groups.append(GROUP_DD(g,g,'false'))


    context = {'groups': groups,'vmslist':vmslist}   
    #context = {'vmslist':vmslist} 
    return render(request,'home/detail.html', context)

@login_required
def vm_stop(request,pk):
    data = dict()
    data['vm_stop'] = False
    vm=VM_STATUS(pk,pk,"running".upper())
    if request.method == 'POST':
        print("POST NOW")
        vm = pk
        post_vm_action(request,setting.CURRENT_RESOURCE_GROUP,vm,"stop")
        time.sleep(5)
        vms=get_resourcegroup_vmstatus()
        vmslist=[]
        for vm in vms:
            vmstatus=vm['status']
            # check if the vm is the vm in action
            if(vm['vm_name']==pk):
                # check the status to make sure it started
                if (vm['status'].lower()!="stopped"):
                    #try to again
                    time.sleep(10)
                    vmsecondrun=get_resourcegroup_vmstatus()
                    for vm2 in vmsecondrun:
                        if(vm2['vm_name']==pk):
                            vmstatus=vm2['status']


            vmslist.append(VM_STATUS(vm['vm_name'],vm['vm_name'],vmstatus.upper()))
        print(vmslist)
        data['form_is_valid'] = True
        data['vm_stop'] = True
        data['html_group_list'] = render_to_string('home/includes/partial_vm_list.html', {
                        'vmslist':vmslist
                })
    else:
        print("Not POST")
        context = {'vm': vm}
        data['html_form'] = render_to_string('home/includes/partial_vm_stop.html', context, request=request)
    return JsonResponse(data)
    
 

@login_required
def vm_start(request,pk):
    data = dict()
    data['vm_start'] = False
    vm=VM_STATUS(pk,pk,"stopped".upper())
    if request.method == 'POST':
        print("POST NOW")
        vm = pk
        post_vm_action(request,setting.CURRENT_RESOURCE_GROUP,vm,"start")
        time.sleep(5)
        vms=get_resourcegroup_vmstatus()

        vmslist=[]
        for vm in vms:
            vmstatus=vm['status']
            # check if the vm is the vm in action
            if(vm['vm_name']==pk):
                # check the status to make sure it started
                if (vm['status'].lower()!="running"):
                    #try to again
                    time.sleep(5)
                    vmsecondrun=get_resourcegroup_vmstatus()
                    for vm2 in vmsecondrun:
                        if(vm2['vm_name']==pk):
                            vmstatus=vm2['status']
                
            vmslist.append(VM_STATUS(vm['vm_name'],vm['vm_name'],vmstatus.upper()))

        print(vmslist)
        data['form_is_valid'] = True
        data['vm_start'] = True
        data['html_group_list'] = render_to_string('home/includes/partial_vm_list.html', {
                        'vmslist':vmslist
                })
    else:
        print("Not POST")
        context = {'vm': vm}
        data['html_form'] = render_to_string('home/includes/partial_vm_start.html', context, request=request)
    return JsonResponse(data)


@login_required
def vm_restart(request,pk):
    data = dict()
    data['vm_restart'] = False
    vm=VM_STATUS(pk,pk,"stopped".upper())
    if request.method == 'POST':
        print("POST NOW")
        vm = pk
        post_vm_action(request,setting.CURRENT_RESOURCE_GROUP,vm,"restart")
        time.sleep(5)
        vms=get_resourcegroup_vmstatus()

        vmslist=[]
        for vm in vms:
            vmstatus=vm['status']
            # check if the vm is the vm in action
            if(vm['vm_name']==pk):
                # check the status to make sure it started
                if (vm['status'].lower()!="running"):
                    #try to again
                    time.sleep(5)
                    vmsecondrun=get_resourcegroup_vmstatus()
                    for vm2 in vmsecondrun:
                        if(vm2['vm_name']==pk):
                            vmstatus=vm2['status']
                
            vmslist.append(VM_STATUS(vm['vm_name'],vm['vm_name'],vmstatus.upper()))

        print(vmslist)
        data['form_is_valid'] = True
        data['vm_restart'] = True
        data['html_group_list'] = render_to_string('home/includes/partial_vm_list.html', {
                        'vmslist':vmslist
                })
    else:
        print("Not POST")
        context = {'vm': vm}
        data['html_form'] = render_to_string('home/includes/partial_vm_restart.html', context, request=request)
    return JsonResponse(data)
