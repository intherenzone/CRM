from django import forms
from organizations.models import Organization
from common.models import Address, Comment

class OrganizationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        assigned_users = kwargs.pop('assigned_to', [])
        super(OrganizationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
        #if self.data.get('status') == 'converted':
        #    self.fields['account_name'].required = True
        self.fields['assigned_to'].queryset = assigned_users
        self.fields['assigned_to'].required = False
        #self.fields['teams'].required = False
        self.fields['phone'].required = False
        self.fields['name'].widget.attrs.update({
            'placeholder': 'name'})
        #self.fields['Name'].widget.attrs.update({
            #'placeholder': 'Name'})
        #self.fields['account_name'].widget.attrs.update({
        #    'placeholder': 'Account Name'})

    class Meta:
        model = Organization
        fields = ('name','assigned_to',
                  'phone', 'email', 'status', 'source', 'website', 'address', 'description'
                  )

    def clean_phone(self):
        client_phone = self.cleaned_data.get('phone', None)
        if client_phone:
            try:
                if int(client_phone) and not client_phone.isalpha():
                    ph_length = str(client_phone)
                    if len(ph_length) < 10 or len(ph_length) > 13:
                        raise forms.ValidationError('Phone number must be minimum 10 Digits and maximum 13 Digits')
            except (ValueError):
                raise forms.ValidationError('Phone Number should contain only Numbers')
            return client_phone
