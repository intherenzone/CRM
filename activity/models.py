from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _

from common.models import Address, Team
from common.utils import LEAD_STATUS, LEAD_SOURCE
from contacts.models import Contact

from django.contrib.auth.models import User
from django.conf import settings

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
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='activity_created_by', on_delete=models.CASCADE)
    activity_type= models.CharField(_("Activity Type"), max_length=255, blank=True, null=True, choices=ACTIVITY_TYPE)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(_("Status of Activity"), max_length=255, blank=True, null=True, choices=LEAD_STATUS)
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="activity_assigned_users")
    teams = models.ManyToManyField(Team)
    

    def __str__(self):
        return self.name
