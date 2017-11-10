from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
from accounts.models import Account
from common.models import User, Address, Team
from common.utils import LEAD_STATUS, LEAD_SOURCE
from organizations.models import Organizations
from activity.models import Activity


class Customer(models.Model):
    title = models.CharField(
        pgettext_lazy("Treatment Pronouns for the customer", "Title"),
         max_length=64, blank=True, null=True)
    first_name=models.CharField(_("First Name"), max_length=255,null=True)
    last_name=models.CharField(_("Last Name"), max_length=255,null=True)
    org = models.ForeignKey(Organizations, related_name='Customer', on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField()
    activity=models.ForeignKey(Activity, related_name='+' ,on_delete=models.CASCADE, blank=True, null=True)
    #startdate=models.DateTimeField(_("Start date"), auto_now_add=True)
    #nddate=models.DateTimeField(_("End date"), auto_now_add=True)
    #created_by = models.ForeignKey(User, related_name='activity_created_by', on_delete=models.CASCADE)
    #activity_type= models.CharField(_("Activity Type"), max_length=255, blank=True, null=True, choices=ACTIVITY_TYPE)
    description = models.TextField(blank=True, null=True)


    phone = models.CharField(max_length=20, null=True, blank=True)
    #account = models.ForeignKey(Account, related_name='Organizations', on_delete=models.CASCADE, blank=True, null=True)
    #status = models.CharField(_("Status of Activity"), max_length=255,
                              #blank=True, null=True, choices=LEAD_STATUS)
    #is_active = models.BooleanField(default=False)
    #source = models.CharField(_("Source of Organizations"), max_length=255,
                        #      blank=True, null=True, choices=LEAD_SOURCE)
    #subOrg=models.CharField(("sub organization"),max_length=200, null=True)
    #contact=models.CharField(("contact"),max_length=200, null=True)
    #address = models.ForeignKey(Address, related_name='organizationsaddress', on_delete=models.CASCADE, null=True, blank=True)
    #website = models.CharField(_("Website"), max_length=255, blank=True, null=True)

    #assigned_to=models.ManyToManyField(User, related_name="org_assigned_users")


    def __str__(self):
        return self.first_name+ self.last_name
