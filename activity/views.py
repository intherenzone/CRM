from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import modelformset_factory
from activity.models import Activity
from activity.forms import ActivityForm
from leads.models import Lead
from contacts.forms import ContactForm
from common.models import User, Address, Comment, Team
from common.utils import LEAD_STATUS, LEAD_SOURCE, INDCHOICES, TYPECHOICES, COUNTRIES
from leads.forms import LeadCommentForm, LeadForm
from accounts.forms import AccountForm
from common.forms import BillingAddressForm
from accounts.models import Account
from planner.models import Event, Reminder
from planner.forms import ReminderForm

# Create your views here.
@login_required
def activity_list(request):
    activity_obj = Activity.objects.all()
    page = request.POST.get('per_page')
    #first_name = request.POST.get('first_name')
    #last_name = request.POST.get('last_name')
    #city = request.POST.get('city')

    email = request.POST.get('email')
    #if first_name:
    #    lead_obj = Lead.objects.filter(first_name__icontains=first_name)
    #if last_name:
    #    lead_obj = Lead.objects.filter(last_name__icontains=last_name)
    #if city:
    #    lead_obj = Lead.objects.filter(address=Address.objects.filter
    #                                   (city__icontains=city))
    if email:
        lead_obj = Lead.objects.filter(email__icontains=email)

    return render(request, 'activity/activity.html', {
        'activity_obj': activity_obj, 'per_page': page})


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
            #address_object = address_form.save()
            #org_obj.address = address_object
            #activity_obj.created_by = request.user
            activity_obj.save()
            #activity_obj.assigned_to.add(*assignedto_list)
            #lead_obj.teams.add(*teams_list)

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
