from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _

from common.models import Address, Team
from common.utils import LEAD_STATUS, LEAD_SOURCE

from django.contrib.auth.models import User
from django.conf import settings

class Organization(models.Model):
    name = models.CharField(pgettext_lazy("Name of Organization", "Name"), max_length=64)
    email = models.EmailField()
    website = models.URLField(_("Website"), max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(_("Status of Organization"), max_length=255,
                              blank=True, null=True, choices=LEAD_STATUS)
    source = models.CharField(_("Source of Organization"), max_length=255,
                              blank=True, null=True, choices=LEAD_SOURCE)
    address = models.ForeignKey(Address, related_name='organization_address', on_delete=models.CASCADE,
                                null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="organization_assigned_to")
    teams = models.ManyToManyField(Team)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='organization_created_by', null= True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
