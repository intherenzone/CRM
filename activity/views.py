from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from activity.models import Activity
from activity.forms import ActivityForm, ActivityCommentForm
from contacts.forms import ContactForm
from common.models import Address, Comment, Team
from common.utils import LEAD_STATUS, LEAD_SOURCE, INDCHOICES, TYPECHOICES, COUNTRIES
from common.forms import BillingAddressForm
from contacts.models import Contact
from common.models import News

from django.contrib.auth.models import User
from django.conf import settings

#for iCalendar
from icalendar import Calendar, Event
from icalendar import vCalAddress, vText
from datetime import datetime
import tempfile, os
import pytz

from django.core.mail import send_mail

# Create your views here.
@login_required
def activity_list(request):
    activity_obj_list = Activity.objects.all()
    page = request.POST.get('per_page')

    name = request.POST.get('name')
    email = request.POST.get('email')
    status = request.POST.get('status')
    activity_type = request.POST.get('activity_type')
    startdate = request.POST.get('startdate')
    enddate = request.POST.get('enddate')
    #created_by = request.POST.get('created_by')
    #assigned_to = request.POST.get('assigned_to')

    if name:
        activity_obj_list = activity_obj_list.filter(name__icontains=name)
    if email:
        activity_obj_list = activity_obj_list.filter(email__icontains=email)
    if status:
        activity_obj_list = activity_obj_list.filter(status__icontains=status)
    if activity_type:
        activity_obj_list = activity_obj_list.filter(activity_type__icontains=activity_type)
    if startdate:
        activity_obj_list = activity_obj_list.filter(startdate__gte=startdate)
    if enddate:
        activity_obj_list = activity_obj_list.filter(enddate__lte=enddate)


    SS = ['In Process', 'Completed', 'Assigned', None]
    activity_obj = sorted(activity_obj_list.order_by('enddate', 'startdate'), key=lambda p: SS.index(p.status))

    return render(request, 'crm/activity/activity.html', {
        'activity_obj': activity_obj, 'per_page': page, 'contacts': contacts})


def send_email(assignedto_list, name, description, action):
    email=[]
    for assigned_to in assignedto_list:
        print(type(assigned_to))
        email.append(assigned_to.email)
    if action == "add":
      send_mail('New activity', 'This email is to notifiy you that activity ' + name + ' is now assigned to you. ' + '\nDescription: '+ description, settings.EMAIL_HOST_USER, email, fail_silently=False)
    elif action == "edit":
        send_mail('Activity ' + name + ' has been changed', 'Dear ' + name + ' one of your assigned activities has been changed. ' + '\nDescription: '+ description, settings.EMAIL_HOST_USER, email, fail_silently=False)
    else:
        send_mail('Activity ' + name + ' has been deleted', 'One of your assigned activities, ' + name + ', has been deleted. ' , settings.EMAIL_HOST_USER, email, fail_silently=False)


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
                news = News(actor = request.user, activity = activity_obj, type = "add_acivity", object_name =activity_obj.name)
                news.save()
                send_email(activity_obj.assigned_to.all(),activity_obj.name,activity_obj.description,"add")
                return HttpResponseRedirect(reverse("activity:add_activity"))
            else:
                news = News(actor = request.user, activity = activity_obj, type = "add_activity", object_name = activity_obj.name)
                news.save()
                send_email(activity_obj.assigned_to.all(),activity_obj.name,activity_obj.description,"add")
                return HttpResponseRedirect(reverse("activity:list"))
        else:
            print(form.errors)
            if request.is_ajax():
                return JsonResponse({'error': True, 'activity_errors': form.errors})
            return render(request, 'crm/activity/create_activity.html', {
                          'activity_form': form,
                          'users': users,
                          'assignedto_list': assignedto_list,
                          'contacts_list': contacts_list,
                          'CREATE': 'CREATE'
                    })
    else:
        return render(request, 'crm/activity/create_activity.html', {
                      'activity_form': form,
                      'users': users,
                      'assignedto_list': assignedto_list,
                      'contacts_list': contacts_list,
                      'CREATE': 'CREATE'
                })

def contacts(request):
    contacts = Contact.objects.all()
    data = {}
    for i in contacts:
        new = {i.pk: i.first_name}
        data.update(new)
    return JsonResponse(data)


@login_required
def view_activity(request, activity_id):
    activity_record = get_object_or_404(Activity, id=activity_id)
    comments = activity_record.activity_comments.all()
    return render(request, 'crm/activity/view_activity.html', {
        'activity_record': activity_record,
        'comments': comments})

@login_required
def remove_activity(request, pk):
    activity = get_object_or_404(Activity, id=pk)
    actor = activity.created_by
    name = activity.name
    news = News(actor=actor, type="delete_activity", object_name=name)
    news.save()
    send_email(activity.assigned_to.all(),activity.name,activity.description,"delete")
    activity.delete()
    if request.is_ajax():
        return JsonResponse({'error': False})
    else:
        return HttpResponseRedirect(reverse('activity:list'))



@login_required
def edit_activity(request,pk):
    activity_obj = get_object_or_404(Activity,id=pk)
    users = User.objects.filter(is_active=True).order_by('email')
    contacts = Contact.objects.all()
    form = ActivityForm(instance=activity_obj, assigned_to=users, contacts=contacts)
    assignedto_list = request.POST.getlist('assigned_to')
    contacts_list = request.POST.getlist("contacts")
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity_obj, assigned_to=users, contacts=contacts)
        # address_form = BillingAddressForm(request.POST)
        if form.is_valid():
            activity_obj = form.save(commit=False)
            activity_obj.created_by = request.user
            activity_obj.save()
            activity_obj.assigned_to.clear()
            activity_obj.assigned_to.add(*assignedto_list)
            activity_obj.contacts.set(contacts_list)
            if request.is_ajax():
                return JsonResponse({'error': False})
            news = News(actor = request.user, activity = activity_obj, type = "edit_activity", object_name =activity_obj.name)
            news.save()
            send_email(activity_obj.assigned_to.all(),activity_obj.name,activity_obj.description,"edit")
            return HttpResponseRedirect(reverse('activity:list'))
        else:
            print(form.errors)
            if request.is_ajax():
                return JsonResponse({'error': True, 'activity_errors': form.errors})
            return render(request, 'crm/activity/create_activity.html', {
                          'activity_form': form,
                          'activity_obj': activity_obj,
                          'users': users,
                          'assignedto_list': assignedto_list,
                          'contacts_list': contacts_list
                    })
    else:
        return render(request, 'crm/activity/create_activity.html', {
                      'activity_form': form,
                      'activity_obj': activity_obj,
                      'users': users,
                      'assignedto_list': assignedto_list,
                      'contacts_list': contacts_list
                })





#Comment

@login_required
def add_comment(request):
    if request.method == 'POST':
        activity = get_object_or_404(Activity, id=request.POST.get('activityid'))
        if request.user in activity.assigned_to.all() or request.user == activity.created_by:
            form = ActivityCommentForm(request.POST)
            if form.is_valid():
                activity_comment = form.save(commit=False)
                activity_comment.comment = request.POST.get('comment')
                activity_comment.commented_by = request.user
                activity_comment.activity = activity
                activity_comment.save()
                news = News(actor = request.user, comment = activity_comment ,type = "comment")
                news.save()
                data = {"comment_id": activity_comment.id, "comment": activity_comment.comment,
                        "commented_on": activity_comment.commented_on,
                        "commented_by": activity_comment.commented_by.email}
                return JsonResponse(data)
            else:
                return JsonResponse({"error": form['comment'].errors})
        else:
            data = {'error': "You Dont Have permissions to Comment"}
            return JsonResponse(data)

@login_required
def edit_comment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        comment_id = request.POST.get("commentid")
        com = get_object_or_404(Comment, id=comment_id)
        form = ActivityCommentForm(request.POST)
        if request.user == com.commented_by:
            if form.is_valid():
                com.comment = comment
                com.save()
                data = {"comment": com.comment, "commentid": comment_id}
                return JsonResponse(data)
            else:
                return JsonResponse({"error": form['comment'].errors})
        else:
            return JsonResponse({"error": "You dont have authentication to edit"})
    else:
        return render(request, "404.html")


@login_required
def remove_comment(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.commented_by:
            comment.delete()
            data = {"cid": comment_id}
            return JsonResponse(data)
        else:
            return JsonResponse({"error": "You Dont have permisions to delete"})
    else:
        return HttpResponse("Something Went Wrong")

#This will syn the calendar everytime calendar app requests from the url for the fiven user
def calendar_syn(request, user):
    activity_obj_list = Activity.objects.all()
    this_user_object = User.objects.filter(username=user)[0]
    this_user_useremail = this_user_object.email
    activities_this_user_is_assigned_to= Activity.objects.filter(assigned_to__email=this_user_useremail)

    #Populating calendar file
    cal= Calendar()
    cal['summary'] = 'CRM-Paradyme Management'
    cal.add('version', '2.0')
    cal.add('X-WR-CALDESC', 'Calendar events for user, ' + this_user_object.username)
    cal.add('X-WR-CALNAME', this_user_object.username + ' Calendar (Paradyme CRM)')
    cal.add('method', 'PUBLISH')
    cal.add('prodid', '-//Paradyme Management//paradymemanagement.com//')
    for activity in activities_this_user_is_assigned_to:
        event = Event()
        event.add('summary', activity.name)
        event.add('description', activity.description)
        event.add('dtstart', activity.startdate)
        event.add('dtend', activity.enddate)
        cal.add_component(event)
    #Create ics file
    response = HttpResponse(cal.to_ical(), content_type='text/calendar')
    response['Content-Disposition'] = 'attachment; filename=' + this_user_object.username +'.ics'
    return response

#Export a ics file for a given activity
@login_required
def export_calendar(request,activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    username = None
    if request.user.is_authenticated:
        username = request.user.username

    cal= Calendar()
    cal['summary'] = 'CRM-Paradyme Management'
    cal.add('version', '2.0')
    cal.add('X-WR-CALDESC', 'Calendar events for user, ' + username)
    cal.add('X-WR-CALNAME', username + ' Calendar (Paradyme CRM)')
    cal.add('method', 'PUBLISH')
    cal.add('prodid', '-//Paradyme Management//paradymemanagement.com//')
    #Create an event
    event = Event()
    event.add('summary', activity.name)
    event.add('dtstart', activity.startdate)
    event.add('dtend', activity.enddate)
    event.add('description', activity.description)
    #organizer = vCalAddress('MAILTO:xxxx@paradymemanagement.com')
    #Add event to calendar
    cal.add_component(event)
    response = HttpResponse(cal.to_ical(), content_type='text/calendar')
    response['Content-Disposition'] = 'attachment; filename=' + activity.name +'.ics'
    return response

#To show the unique calendar url for the user
@login_required
def calendar_url(request):
    #Get current username and email
    username = None
    useremail = None
    if request.user.is_authenticated:
        username = request.user.username
        useremail = request.user.email

    user_url = str(reverse('activity:calendar_syn', args=[username]))

    return render(request, 'crm/activity/calendar_url.html', {
        'user_url' : user_url,
        })
