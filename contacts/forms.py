from django import forms
from contacts.models import Contact
from common.models import Comment


class ContactForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        assigned_users = kwargs.pop('assigned_to', [])
        contact_org = kwargs.pop('organization', [])
        super(ContactForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
        self.fields['description'].widget.attrs.update({
            'rows': '6'})
        self.fields['assigned_to'].queryset = assigned_users
        self.fields['organization'].queryset = contact_org
        self.fields['organization'].required = False
        self.fields['assigned_to'].required = False
        self.fields['teams'].required = False

    class Meta:
        model = Contact
        fields = (
            'assigned_to', 'organization', 'teams', 'first_name', 'last_name', 'email', 'phone', 'address', 'description'
        )

    def format_phone(phone):
        phone_length = len(phone)
        if phone_length == 11:
            new_phone = phone[:1] + ' (' + phone[1:4] + ') ' + phone[4:7] + '-' + phone[7:]
        elif phone_length == 12:
            new_phone = phone[:2] + ' (' + phone[2:5] + ') ' + phone[5:8] + '-' + phone[8:]
        elif phone_length == 13:
            new_phone = phone[:3] + ' (' + phone[3:6] + ') ' + phone[6:9] + '-' + phone[9:]
        else:
            new_phone = '(' + phone[0:3] + ') ' + phone[3:6] + '-' + phone[6:]
        return phone

    def clean_phone(self):
        client_phone = self.cleaned_data.get('phone', None)
        try:
            if int(client_phone) and not client_phone.isalpha():
                ph_length = str(client_phone)
                if len(ph_length) < 10 or len(ph_length) > 13:
                    raise forms.ValidationError('Phone number must be minimum 10 Digits and maximum of 13 Digits')
        except (ValueError):
            raise forms.ValidationError('Phone Number should contain only Numbers')

        # COMMENTED OUT BECAUSE FILTER WON'T FIND NUMBERS I.E. 7035011932 -> (703) 501-1932, FILTER WON'T FIND IF USER ENTERS 703501...
        # phone_length = len(client_phone)
        # if phone_length == 11:
        #     new_phone = client_phone[:1] + ' (' + client_phone[1:4] + ') ' + client_phone[4:7] + '-' + client_phone[7:]
        # elif phone_length == 12:
        #     new_phone = client_phone[:2] + ' (' + client_phone[2:5] + ') ' + client_phone[5:8] + '-' + client_phone[8:]
        # elif phone_length == 13:
        #     new_phone = client_phone[:3] + ' (' + client_phone[3:6] + ') ' + client_phone[6:9] + '-' + client_phone[9:]
        # else:
        #     new_phone = '(' + client_phone[0:3] + ') ' + client_phone[3:6] + '-' + client_phone[6:]
        #
        # client_phone = new_phone
        return client_phone


class ContactCommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=64, required=True)

    class Meta:
        model = Comment
        fields = ('comment', 'contact', 'commented_by')
