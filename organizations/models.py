from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
from common.models import User, Address, Team
from common.utils import LEAD_STATUS, LEAD_SOURCE

class Organization(models.Model):
    name = models.CharField(("Name"), max_length=255)
    website = models.URLField(_("Website"), max_length=255, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(_("Status of Organization"), max_length=255,
                              blank=True, null=True, choices=LEAD_STATUS)
    source = models.CharField(_("Source of Organization"), max_length=255,
                              blank=True, null=True, choices=LEAD_SOURCE)
    address = models.ForeignKey(Address, related_name='organization_address', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    assigned_to=models.ManyToManyField(User, related_name="org_assigned_users")


    def __str__(self):
        return self.Name
