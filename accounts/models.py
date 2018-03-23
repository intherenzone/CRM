from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _

from common.models import Address, Team
from common.utils import INDCHOICES

from django.conf import settings

class Account(models.Model):
    first_name = models.CharField(_("First name"), max_length=255)
    last_name = models.CharField(_("Last name"), max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    industry = models.CharField(_("Industry Type"), max_length=255, choices=INDCHOICES, blank=True, null=True)
    billing_address = models.ForeignKey(Address, related_name='account_billing_address', on_delete=models.CASCADE, blank=True, null=True)
    shipping_address = models.ForeignKey(Address, related_name='account_shipping_address', on_delete=models.CASCADE, blank=True, null=True)
    website = models.URLField(_("Website"), blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='account_assigned_to')
    teams = models.ManyToManyField(Team)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='account_created_by', on_delete=models.CASCADE)
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
