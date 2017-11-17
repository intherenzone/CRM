from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import modelformset_factory
from organizations.models import Organization
#from leads.models import Lead
from contacts.forms import ContactForm
from common.models import User, Address, Comment, Team
from common.utils import LEAD_STATUS, LEAD_SOURCE, INDCHOICES, TYPECHOICES, COUNTRIES
from organizations.forms import OrganizationForm
from accounts.forms import AccountForm
from common.forms import BillingAddressForm
from accounts.models import Account
from planner.models import Event, Reminder
from planner.forms import ReminderForm

# Create your views here.

@login_required
def organizations_list(request):
    org_obj = Organization.objects.all()
    page = request.POST.get('per_page')
    Name = request.POST.get('Name')
    city = request.POST.get('city')
    email = request.POST.get('email')
    if Name:
        org_obj = Organization.objects.filter(Name__icontains=Name)
    #if last_name:
    #    lead_obj = Lead.objects.filter(last_name__icontains=last_name)
    if city:
        org_obj = Organization.objects.filter(address=Address.objects.filter
                                       (city__icontains=city))
    if email:
        org_obj = Organization.objects.filter(email__icontains=email)

    return render(request, 'organizations/organizations.html', {
        'org_obj': org_obj, 'per_page': page})



@login_required
def add_org(request):
    accounts = Account.objects.all()
    users = User.objects.filter(is_active=True).order_by('email')
    #teams = Team.objects.all()
    assignedto_list = request.POST.getlist('assigned_to')
    #teams_list = request.POST.getlist('teams')
    org_account = request.POST.get('account_name')
    org_email = request.POST.get('email')
    org_phone = request.POST.get('phone')
    form = OrganizationForm(assigned_to=users)
    address_form = BillingAddressForm()
    if request.method == 'POST':
        form = OrganizationsForm(request.POST, assigned_to=users)
        address_form = BillingAddressForm(request.POST)
        if address_form.is_valid():
            org_obj = form.save(commit=False)
            address_object = address_form.save()
            org_obj.address = address_object
            org_obj.created_by = request.user
            org_obj.save()
            org_obj.assigned_to.add(*assignedto_list)
            #lead_obj.teams.add(*teams_list)
            if request.POST.get('status') == "converted":
                Account.objects.create(
                    created_by=request.user, name=org_account,
                    email=org_email, phone=org_phone
                )
            if request.POST.get("savenewform"):
                return HttpResponseRedirect(reverse("organizations:add_org"))
            else:
                return HttpResponseRedirect(reverse('organizations:list'))
        else:
            return render(request, 'organizations/create_org.html', {
                          'org_form': form, 'address_form': address_form,
                          'accounts': accounts,
                          'users': users,
                          'status': LEAD_STATUS, 'source': LEAD_SOURCE,
                          'assignedto_list': assignedto_list})
    else:
        return render(request, 'organizations/create_org.html', {
                      'org_form': form, 'address_form': address_form,
                      'accounts': accounts,
                      'users': users, 'status': LEAD_STATUS, 'source': LEAD_SOURCE})
