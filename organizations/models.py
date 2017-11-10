from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
# Create your models here.
from accounts.models import Account
from common.models import User, Address, Team
from common.utils import LEAD_STATUS, LEAD_SOURCE

class Organizations(models.Model):
    #title = models.CharField(
    #    pgettext_lazy("Treatment Pronouns for the customer", "Title"),
    #    max_length=64, blank=True, null=True)
    Name = models.CharField(("Name"), max_length=255)
    email = models.EmailField()

    phone = models.CharField(max_length=20, null=True, blank=True)
    account = models.ForeignKey(Account, related_name='Organizations', on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(_("Status of Organizations"), max_length=255,
                              blank=True, null=True, choices=LEAD_STATUS)
    source = models.CharField(_("Source of Organizations"), max_length=255,
                              blank=True, null=True, choices=LEAD_SOURCE)
    subOrg=models.CharField(("sub organization"),max_length=200, null=True)
    contact=models.CharField(("contact"),max_length=200, null=True)
    address = models.ForeignKey(Address, related_name='organizationsaddress', on_delete=models.CASCADE, null=True, blank=True)
    website = models.CharField(_("Website"), max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    assigned_to=models.ManyToManyField(User, related_name="org_assigned_users")


    def __str__(self):
        return self.Name
