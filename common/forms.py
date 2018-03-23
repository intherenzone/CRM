from django import forms
from common.models import *
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CRMUser
        fields = ('email', 'username')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        #user.is_staff = self.cleaned_data["is_staff"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CRMUser
        fields = ('email', 'password', 'username', 'is_active', 'is_admin','is_staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class BillingAddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ('address_line', 'street', 'city', 'state', 'postcode', 'country')

    def __init__(self, *args, **kwargs):
        super(BillingAddressForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
        self.fields['address_line'].widget.attrs.update({
            'placeholder': 'Address Line'})
        self.fields['street'].widget.attrs.update({
            'placeholder': 'Street'})
        self.fields['city'].widget.attrs.update({
            'placeholder': 'City'})
        self.fields['state'].widget.attrs.update({
            'placeholder': 'State'})
        self.fields['postcode'].widget.attrs.update({
            'placeholder': 'Postcode'})
        self.fields["country"].choices = [("", "--Country--"), ] + list(self.fields["country"].choices)[1:]


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('address_line', 'street', 'city', 'state', 'postcode', 'country')

    def __init__(self, *args, **kwargs):
        super(ShippingAddressForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
        self.fields['address_line'].widget.attrs.update({
            'placeholder': 'Address Line'})
        self.fields['street'].widget.attrs.update({
            'placeholder': 'Street'})
        self.fields['city'].widget.attrs.update({
            'placeholder': 'City'})
        self.fields['state'].widget.attrs.update({
            'placeholder': 'State'})
        self.fields['postcode'].widget.attrs.update({
            'placeholder': 'Postcode'})
        self.fields["country"].choices = [("", "--Country--"), ] + list(self.fields["country"].choices)[1:]
