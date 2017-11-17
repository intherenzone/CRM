import json

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from contacts.models import Contact
from activity.models import Activity
from activity.forms import ActivityForm
from common.models import User, Address, Comment, Team
from common.utils import LEAD_STATUS, LEAD_SOURCE, INDCHOICES, TYPECHOICES, COUNTRIES

# Create your views here.
@login_required
def activity_list(request):
    activity_list = Activity.objects.all().prefetch_related("contacts")
    contacts = Contact.objects.all()
    page = request.POST.get('per_page')
    activity_name = request.POST.get('name')
    activity_contact = request.POST.get('contacts')
    activity_email = request.POST.get('email')
    #if first_name:
    #    lead_obj = Lead.objects.filter(first_name__icontains=first_name)
    #if last_name:
    #    lead_obj = Lead.objects.filter(last_name__icontains=last_name)
    #if city:
    #    lead_obj = Lead.objects.filter(address=Address.objects.filter
    #                                   (city__icontains=city))
    # if email:
    #     lead_obj = Lead.objects.filter(email__icontains=email)

    return render(request, 'activity/activity.html', {
        'activity_list': activity_list,
        'contacts': contacts,
        'per_page': page
    })


@login_required
def add_activity(request):
    #accounts = Account.objects.all()
    #users = User.objects.filter(is_active=True).order_by('email')
    #teams = Team.objects.all()
    #assignedto_list = request.POST.getlist('assigned_to')
    #teams_list = request.POST.getlist('teams')
    #org_account = request.POST.get('account_name')
    activity_email = request.POST.get('email')
    #_phone = request.POST.get('phone')
    form = ActivityForm()
    #address_form = BillingAddressForm()
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        #address_form = BillingAddressForm(request.POST)
        if form.is_valid():
            activity_obj = form.save(commit=False)
            activity_obj.save()
            if request.POST.get("savenewform"):
                return HttpResponseRedirect(reverse("activity:add_activity"))
            else:
                return HttpResponseRedirect(reverse('activity:list'))
        else:
            return render(request, 'activity/create_activity.html', {
                          'activity_form': form}) #address_form': address_form,})
    else:
        return render(request, 'activity/create_activity.html', {
                      'activity_form': form
                      })
