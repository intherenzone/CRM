from django import forms
from activity.models import Activity
from common.models import Address, Comment

class ActivityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        #assigned_users = kwargs.pop('assigned_to', [])
        super(ActivityForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
        #if self.data.get('status') == 'converted':
        #    self.fields['account_name'].required = True
        #self.fields['assigned_to'].queryset = assigned_users
        #self.fields['assigned_to'].required = False
        #self.fields['teams'].required = False
        #self.fields['phone'].required = False
        #elf.fields['first_name'].widget.attrs.update({
    #        'placeholder': 'First Name'})
    #    self.fields['last_name'].widget.attrs.update({
    #        'placeholder': 'Last Name'})
    #    self.fields['account_name'].widget.attrs.update({
    #        'placeholder': 'Account Name'})

    class Meta:
        model = Activity
        fields = ('org', 'assigned_to','email', 'startdate', 'enddate', 'created_by', 'activity_type',
                  'description','Name','status'
                  )
