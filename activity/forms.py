from django import forms
from activity.models import Activity
from contacts.models import Contact
from common.models import Address, Team
from organizations.models import Organization
from common.utils import LEAD_STATUS, LEAD_STATUS
from common.models import Comment

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
        # self.fields['first_name'].widget.attrs.update({
        #        'placeholder': 'First Name'})
        #    self.fields['last_name'].widget.attrs.update({
        #        'placeholder': 'Last Name'})
        #    self.fields['account_name'].widget.attrs.update({
        #        'placeholder': 'Account Name'})

    class Meta:
        model = Activity
        fields = (
            'name', 'contacts', 'startdate', 'enddate', 'activity_type', 'description', 'status', 'assigned_to'
        )

class ActivityCommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=64, required=True)

    class Meta:
        model = Comment
        fields = ('comment', 'activity', 'commented_by')
