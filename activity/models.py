from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
from common.models import User, Address, Team
from common.utils import LEAD_STATUS, LEAD_SOURCE
from contacts.models import Contact

ACTIVITY_TYPE=(
   ('Email', 'Email'),
   ('Phone Call','Phone Call'),
   ('Meeting','Meeting'),

)

class Activity(models.Model):
    name = models.CharField(("Activity Name"), null = True, max_length=255)
    email = models.EmailField()
    contacts = models.ManyToManyField(Contact)
    startdate = models.DateTimeField(_("Start date"), auto_now_add=False)
    enddate = models.DateTimeField(_("End date"), auto_now_add=False)
    created_by = models.ForeignKey(User, related_name='activity_created_by', on_delete=models.CASCADE)
    activity_type= models.CharField(_("Activity Type"), max_length=255, blank=True, null=True, choices=ACTIVITY_TYPE)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(_("Status of Activity"), max_length=255,
                              blank=True, null=True, choices=LEAD_STATUS)
    assigned_to = models.ManyToManyField(User, related_name="activity_assigned_users")


    def __str__(self):
        return self.name
