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
from contacts.models import Contact

# Create your views here.
@login_required
def activity_list(request):
    activity_obj_list = Activity.objects.all()
    page = request.POST.get('per_page')

    email = request.POST.get('email')
    status = request.POST.get('status')
    activity_type = request.POST.get('activity_type')
    startdate = request.POST.get('startdate')
    enddate = request.POST.get('enddate')
    #created_by = request.POST.get('created_by')
    #assigned_to = request.POST.get('assigned_to')

    if email:
        activity_obj_list = activity_obj_list.filter(email__icontains=email)
    if status:
        activity_obj_list = activity_obj_list.filter(status__icontains=status)
    if activity_type:
        activity_obj_list = activity_obj_list.filter(activity_type__icontains=activity_type)
    if startdate:
        activity_obj_list = activity_obj_list.filter(startdate__icontains=startdate)
    if enddate:
        activity_obj_list = activity_obj_list.filter(enddate__icontains=enddate)


    SS = ['in process', 'converted', 'recycled', 'assigned', 'dead']
    activity_obj = sorted(activity_obj_list.order_by('enddate', 'startdate'), key=lambda p: SS.index(p.status))

    return render(request, 'activity/activity.html', {
        'activity_obj': activity_obj, 'per_page': page, 'contacts': contacts,})


@login_required
def add_activity(request):
    users = User.objects.filter(is_active=True).order_by('email')
    contacts = Contact.objects.all()
    form = ActivityForm(assigned_to=users, contacts=contacts)
    assignedto_list = request.POST.getlist('assigned_to')
    contacts_list = request.POST.getlist("contacts")


    if request.method == 'POST':
        form = ActivityForm(request.POST,assigned_to=users, contacts=contacts)
        #address_form = BillingAddressForm(request.POST)
        if form.is_valid():
            activity_obj = form.save(commit=False)
            activity_obj.created_by = request.user
            activity_obj.save()
            activity_obj.assigned_to.add(*assignedto_list)
            activity_obj.contacts.add(*contacts_list)
            if request.is_ajax():
                return JsonResponse({'error': False})
            if request.POST.get("savenewform"):
                return HttpResponseRedirect(reverse("activities:save"))
            else:
                return HttpResponseRedirect(reverse("activities:list"))
        else:
            print(form.errors)
            if request.is_ajax():
                return JsonResponse({'error': True, 'activity_errors': form.errors})
            return render(request, 'activity/create_activity.html', {
                          'activity_form': form,
                          'users': users,
                          'assignedto_list': assignedto_list,
                          'contacts_list': contacts_list
                    })
    else:
        return render(request, 'activity/create_activity.html', {
                      'activity_form': form,
                      'users': users,
                      'assignedto_list': assignedto_list,
                      'contacts_list': contacts_list
                })

def contacts(request):
    contacts = Contact.objects.all()
    data = {}
    for i in contacts:
        new = {i.pk: i.first_name}
        data.update(new)
    return JsonResponse(data)
