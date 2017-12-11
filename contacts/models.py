from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from common.models import Address, User, Team
from organizations.models import Organization


class Contact(models.Model):
    first_name = models.CharField(_("First name"), max_length=255)
    last_name = models.CharField(_("Last name"), max_length=255)
    title = models.CharField(pgettext_lazy("Contact Title", "Title"), max_length=64, blank=True, null=True)
    organization = models.ForeignKey(Organization, related_name='organization_contacts', on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.ForeignKey(Address, related_name='adress_contacts', on_delete=models.CASCADE, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    assigned_to = models.ManyToManyField(User, related_name='contact_assigned_users')
    teams = models.ManyToManyField(Team)
    created_by = models.ForeignKey(User, related_name='contact_created_by', on_delete=models.CASCADE)
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    is_active = models.BooleanField(default=False)
    #notes = models.TextField(blank = True, null = True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
