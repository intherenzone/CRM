from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

from common.utils import COUNTRIES

from django.contrib.auth.models import User
from django.conf import settings

# class CRMUser(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=100, unique=True)
#     email = models.EmailField(max_length=255, unique=True)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(('date joined'), auto_now_add=True)
#
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
#
#     objects = UserManager()
#
#     def get_short_name(self):
#         return self.username
#
#     def __unicode__(self):
#         return self.email
#
#     def has_perm(self, perm, obj=None):
#         if CRMUser.is_admin:
#             return True
#         else:
#             return False
#
#     def has_module_perms(self, app_label):
#         if CRMUser.is_admin:
#             return True
#         else:
#             return False



class Address(models.Model):
    address_line = models.CharField(_("Address"), max_length=255, blank=True, null=True)
    street = models.CharField(_("Street"), max_length=55, blank=True, null=True)
    city = models.CharField(_("City"), max_length=255, blank=True, null=True)
    state = models.CharField(_("State"), max_length=255, blank=True, null=True)
    postcode = models.CharField(_("Post/Zip-code"), max_length=64, blank=True, null=True)
    country = models.CharField(max_length=3, choices=COUNTRIES, blank=True, null=True)

    def __str__(self):
        return self.city


class Team(models.Model):
    name = models.CharField(max_length=55)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name


class Comment(models.Model):
    case = models.ForeignKey('cases.Case', blank=True, null=True, related_name="cases", on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    commented_on = models.DateTimeField(auto_now_add=True)
    commented_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    account = models.ForeignKey(
        'accounts.Account', blank=True, null=True, related_name="accounts_comments", on_delete=models.CASCADE)
    lead = models.ForeignKey('leads.Lead', blank=True, null=True, related_name="leads", on_delete=models.CASCADE)
    opportunity = models.ForeignKey(
        'oppurtunity.Opportunity', blank=True, null=True, related_name="opportunity_comments", on_delete=models.CASCADE)
    contact = models.ForeignKey(
        'contacts.Contact', blank=True, null=True, related_name="contact_comments", on_delete=models.CASCADE)
    organization = models.ForeignKey(
        'organizations.Organization', blank=True, null=True, related_name="organization_comments", on_delete=models.CASCADE)
    activity = models.ForeignKey(
        'activity.Activity', blank=True, null=True, related_name="activity_comments", on_delete=models.CASCADE)

    def get_files(self):
        return Comment_Files.objects.filter(comment_id=self)


class Comment_Files(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now_add=True)
    comment_file = models.FileField("File", upload_to="comment_files", default='')

    def get_file_name(self):
        if self.comment_file:
            return self.comment_file.path.split('/')[-1]
        else:
            return None


class News(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=255)
    object_name = models.CharField(max_length=255, blank=True, null=True)
    activity = models.ForeignKey(
        'activity.Activity', blank=True, null=True, related_name="activity_news", on_delete=models.CASCADE)
    contact = models.ForeignKey(
        'contacts.Contact', blank=True, null=True, related_name="contact_news", on_delete=models.CASCADE)
    organization = models.ForeignKey(
        'organizations.Organization', blank=True, null=True, related_name="organization_news", on_delete=models.CASCADE)
    comment = models.ForeignKey(
        'common.Comment', blank=True, null=True, related_name="comment_news", on_delete=models.CASCADE)
