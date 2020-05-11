from django import forms
from bootstrap_datepicker_plus import DateTimePickerInput
from .models import Group
from .schedules import get_resourcegroup_vmlist
from home import setting
from django.utils.functional import lazy

def get_resourcegroup_choices():
    print('get resoucegroup list')
    choices =[]
    for r in setting.RESOURCE_GROUPS:
        l=[]
        l.append(r)
        l.append(r)
        choices.append(l)

    print(choices)
    return choices

def get_vm_list_choices():

    choices = get_resourcegroup_vmlist(setting.SUBSCRIPTION_ID,setting.RESOURCE_GROUP)
    print('choices are')
    print(choices)
    return choices

    
class GroupForm(forms.ModelForm):
    choices1 =[[1,"test1"],[2,"test2"],[3,"test3"]]
    vm_list = forms.MultipleChoiceField(choices=choices1, widget=forms.CheckboxSelectMultiple(),required=False)
    #group_name = forms.Select(choices=choices1)

    class Meta:
       
        model = Group
        #group_name,group_schid,group_desc,start_time,shutdown_time,schedule_end,vm_list,recurring,time_zone,
        fields = ('group_name','group_desc', 'start_time',  'shutdown_time','schedule_end','recurring','time_zone','vm_list')
        widgets = {
           'start_time': DateTimePickerInput(), 
            'shutdown_time': DateTimePickerInput(), 
            'schedule_end': DateTimePickerInput(),
            #'vm_list': forms.CheckboxSelectMultiple(choices=get_list())
        }
        



    def __init__(self, *args, **kwargs):
        print("init group")
        super(GroupForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        print(instance)
        if instance :
            print("inside instance")
            self.fields['group_desc'].label = 'Schedule Name'
            self.fields['shutdown_time'].label = 'VM Power OFF Start Schedule'
            self.fields['start_time'].label = 'VM Power ON Start Schedule' 
            self.fields['schedule_end'].label = 'VM Power ON End Schedule' 
            self.fields['vm_list'].label = 'Select VM Name(s)' 
            self.fields['vm_list'].widget.attrs['class'] ='checkboxlist'
            self.fields['recurring'].label = 'Is Recurring' 
            self.fields['group_name'].widget.attrs['readonly'] = True
            self.fields['vm_list'].choices = lazy(get_vm_list_choices,list)()



                

