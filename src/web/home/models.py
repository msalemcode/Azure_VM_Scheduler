from __future__ import unicode_literals

from django.db import models
  



TIMEZON_CHOICES = [
    ('America/Los_Angeles', 'US - Pacific Time'),
    ('America/Chicago', 'US - Central Time'),
    ('America/New_York','US - Eastern Time'),
    ('UTC','UTC')
]

SCHEDULE_TYPE = [
    ('1', 'Recurring'),
    ('0', 'One Time')
]
class Group(models.Model):
   

    group_name = models.CharField(max_length=250)#resource group
    group_schid=models.CharField(max_length=250)#sch id
    group_desc = models.CharField(max_length=50)#sch desc
    start_time = models.DateTimeField( )
    shutdown_time = models.DateTimeField()
    schedule_end = models.DateTimeField()
    vm_list = models.CharField(max_length=1500)
    recurring = models.CharField(max_length=1,choices=SCHEDULE_TYPE) 
    time_zone = models.CharField(max_length=50, choices=TIMEZON_CHOICES)
    



class Subscription(models.Model):
    subscription_id = models.CharField(max_length=150)
    display_name  = models.CharField(max_length=50)

 
class VMlist(models.Model):
    
    display_name  = models.CharField(max_length=150)
    checked = models.CharField(max_length=7)   


class VM_STATUS(models.Model):
    vm_name  = models.CharField(max_length=250)
    vm_status = models.CharField(max_length=10)    

class GROUP_DD(models.Model):
    group  = models.CharField(max_length=250)
    selected = models.CharField(max_length=10)      