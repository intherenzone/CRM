from django import forms
from activity.models import Activity
from contacts.models import Contact
from common.models import Address, User, Team
from organizations.models import Organization
from common.utils import LEAD_STATUS, LEAD_STATUS

ACTIVITY_TYPE=(
   ('Email', 'Email'),
   ('Phone Call','Phone Call'),
   ('Meeting','Meeting'),

)

class ActivityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        assigned_users = kwargs.pop('assigned_to', [])
        activity_contacts = kwargs.pop('contacts', [])
        super(ActivityForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
        # if self.data.get('status') == 'converted':
        #    self.fields['account_name'].required = True
        self.fields['assigned_to'].queryset = assigned_users
        self.fields['assigned_to'].required = False
        self.fields['contacts'].queryset = activity_contacts
        self.fields['description'].widget.attrs.update({
            'rows': '6'})
        # self.fields['teams'].required = False
        # self.fields['phone'].required = False
        # elf.fields['first_name'].widget.attrs.update({
        #        'placeholder': 'First Name'})
        #    self.fields['last_name'].widget.attrs.update({
        #        'placeholder': 'Last Name'})
        #    self.fields['account_name'].widget.attrs.update({
        #        'placeholder': 'Account Name'})

    class Meta:
        model = Activity
        fields = (
            'name', 'email', 'contacts', 'startdate', 'enddate', 'activity_type', 'description', 'status', 'assigned_to'
        )
