from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import modelformset_factory

from customer.models import Customer
from contacts.forms import ContactForm
from common.models import User, Address, Comment, Team
from common.utils import LEAD_STATUS, LEAD_SOURCE, INDCHOICES, TYPECHOICES, COUNTRIES
from customer.forms import CustomerForm
from accounts.forms import AccountForm
from common.forms import BillingAddressForm
from accounts.models import Account
from planner.models import Event, Reminder
from planner.forms import ReminderForm

# CRUD Operations Start


@login_required
def customer_list(request):
    customer_obj = Customer.objects.all()
    page = request.POST.get('per_page')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    #city = request.POST.get('city')
    email = request.POST.get('email')
    if first_name:
        lead_obj = Lead.objects.filter(first_name__icontains=first_name)
    if last_name:
        lead_obj = Lead.objects.filter(last_name__icontains=last_name)
    #if city:
    #    lead_obj = Lead.objects.filter(address=Address.objects.filter
    #                                   (city__icontains=city))
    if email:
        lead_obj = Lead.objects.filter(email__icontains=email)

    return render(request, 'customers/customers.html', {
        'customer_obj': customer_obj, 'per_page': page})


@login_required
def add_customer(request):
    #accounts = Account.objects.all()
    #users = User.objects.filter(is_active=True).order_by('email')
    #teams = Team.objects.all()
    #assignedto_list = request.POST.getlist('assigned_to')
    #teams_list = request.POST.getlist('teams')
    #lead_account = request.POST.get('account_name')
    customer_email = request.POST.get('email')
    customer_phone = request.POST.get('phone')
    form = CustomerForm()
    #address_form = BillingAddressForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        #address_form = BillingAddressForm(request.POST)
        if form.is_valid():
            customer_obj = form.save(commit=False)
            #address_object = address_form.save()
            #lead_obj.address = address_object
            #lead_obj.created_by = request.user
            customer_obj.save()
            #lead_obj.assigned_to.add(*assignedto_list)
            #lead_obj.teams.add(*teams_list)

            if request.POST.get("savenewform"):
                return HttpResponseRedirect(reverse("customer:add_customer"))
            else:
                return HttpResponseRedirect(reverse('customer:list'))
        else:
            return render(request, 'customers/create_customer.html', {
                          'customer_form': form})
    else:
        return render(request, 'customers/create_customer.html', {
                      'customer_form': form})
