from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from common.forms import *
from common.models import *
from django.db.models import Q

from django.contrib.auth.models import User
from django.conf import settings

from contacts.models import Contact
from activity.models import *
from organizations.models import *
from common.utils import LEAD_STATUS, LEAD_SOURCE

from plotly.offline import plot
import plotly.graph_objs as go
from datetime import datetime

@login_required
def home(request):
    # Get user's contacts
    contacts = Contact.objects.filter(assigned_to=request.user)

    # Get user's organizations
    organizations = Organization.objects.filter(assigned_to=request.user)

    # Get user's teams
    teams = Team.objects.filter(members__id = request.user.id)
    # Get each team's contacts
    teams_contacts = []
    for team in teams:
        teams_contacts.append(Contact.objects.filter(teams=team))
    # map teams to their contacts
    teams_to_contacts = zip(teams, teams_contacts)

    #get the news object
    newsfeed = News.objects.order_by('-date')[0:15]

    # count activity types for graphing
    activity_types = []
    activity_type_counts = []
    user_activity_type_counts = []

    for activity_type in ACTIVITY_TYPE:
        activity_types.append(activity_type[0]) # get each type
        activity_type_counts.append(Activity.objects.filter(activity_type=activity_type[0]).count()) # get count of each type
        user_activity_type_counts.append(Activity.objects.filter(assigned_to=request.user,activity_type=activity_type[0]).count())
     #Donut Pie chart Activity Type
    figa = {
        "data": [
            {
                "values": user_activity_type_counts,
                "labels": activity_types,
                "text": user_activity_type_counts,
                "textposition": "inside",
                "domain": {"x": [0, .48]},
                "hoverinfo": "label+percent",
                "hole": .4,
                "type": "pie"

            },
            {
                "values": activity_type_counts,
                "labels": activity_types,
                "text": activity_type_counts,
                "textposition": "inside",
                "domain": {"x": [.52, 1]},
                "hoverinfo": "label+percent",
                "hole": .4,
                "type": "pie"
            }],
        "layout": {
            "title": "Activity Type",
            "annotations": [
                {
                    "font": {
                        "size": 12
                    },
                    "showarrow": False,
                    "text": "You",
                    "x": 0.22,
                    "y": 0.5
                },
                {
                    "font": {
                        "size": 12
                    },
                    "showarrow": False,
                    "text": "Company",
                    "x": 0.805,
                    "y": 0.5

                }
            ]
        }
    }
    activity_type_chart = plot(figa, output_type='div')

    # Count statuses for graphing
    statuses = []
    status_counts = []
    user_status_counts = []
    for status in LEAD_STATUS:
        statuses.append(status[0])
        status_counts.append(Activity.objects.filter(status=status[0]).count())
        user_status_counts.append(Activity.objects.filter(assigned_to=request.user, status=status[0]).count())
    # create status pie chart
    fig_stat = {
        "data": [
            {
                "values": user_status_counts,
                "labels": statuses,
                "text": user_status_counts,
                "textposition": "inside",
                "domain": {"x": [0, .48]},
                "hoverinfo": "label+percent",
                "hole": .4,
                "type": "pie"
            },
            {
                "values": status_counts,
                "labels": statuses,
                "text": status_counts,
                "textposition": "inside",
                "domain": {"x": [.52, 1]},
                "hoverinfo": "label+percent",
                "hole": .4,
                "type": "pie"
            }],
        "layout": {
            "title": "Activity Status",
            "annotations": [
                {
                    "font": {
                        "size": 12
                    },
                    "showarrow": False,
                    "text": "You",
                    "x": 0.22,
                    "y": 0.5
                },
                {
                    "font": {
                        "size": 12
                    },
                    "showarrow": False,
                    "text": "Company",
                    "x": 0.805,
                    "y": 0.5
                }
            ]
        }
    }
    status_chart = plot(fig_stat, output_type='div')


    return render(request , 'crm/index.html',
        {
            "contacts" : contacts,
            "organizations" : organizations,
            "teams_to_contacts" : teams_to_contacts,
            "activity_type_chart" : activity_type_chart,
            "status_chart" : status_chart,
            "newsfeed":newsfeed,
    })


@csrf_exempt
def login_crm(request):
    print('login')
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
    return render(request, 'crm/login.html')

def register_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
            )
            user.save()
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
    variables = {
        'form': form
    }
    return render(request, 'crm/registration.html', variables)

def newsfeed(request):
    newsfeed = News.objects.order_by('-date').all()
    page = request.POST.get('per_page')

    username = request.POST.get('username')
    module = request.POST.get('module')
    action_type = request.POST.get('action_type')
    startdate = request.POST.get('startdate')
    enddate = request.POST.get('enddate')

    if username:
        newsfeed = newsfeed.filter(actor__username__icontains=username)
    if module=='activity':
        newsfeed = newsfeed.filter(activity__isnull = False)
    elif module=='contact':
        newsfeed = newsfeed.filter(contact__isnull=False)
    elif module=='organization':
        newsfeed = newsfeed.filter(organization__isnull=False)
    elif module=='comment':
        newsfeed = newsfeed.filter(comment__isnull=False)
    if action_type:
        newsfeed = newsfeed.filter(type__icontains=action_type)
    if startdate:
        newsfeed = newsfeed.filter(date__gte=startdate)
    if enddate:
        newsfeed = newsfeed.filter(date__lte=enddate)

    return render(request, 'crm/newsfeed.html', {
        'newsfeed': newsfeed
        })
