from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from common.forms import *
from common.models import *

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

    # count activity types for graphing
    activity_types = []
    activity_type_counts = []
    for activity_type in ACTIVITY_TYPE:
        activity_types.append(activity_type[0]) # get each type
        activity_type_counts.append(Activity.objects.filter(activity_type=activity_type[0]).count()) # get count of each type
    # create activity type pie chart
    activity_type_trace = go.Pie(labels=activity_types, values=activity_type_counts,
               hoverinfo='label+percent' , textinfo='value',
               textfont=dict(size=20),
               )
    data = go.Data([activity_type_trace])
    layout = go.Layout(title='Activity Type',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
    fig = go.Figure(data=data,layout=layout)
    activity_type_chart = plot(fig, output_type = 'div')

    # Count statuses for graphing
    statuses = []
    status_counts = []
    for status in LEAD_STATUS:
        statuses.append(status[0])
        status_counts.append(Activity.objects.filter(status=status[0]).count())
    # create status pie chart
    status_trace = go.Pie(labels=statuses, values=status_counts,
               hoverinfo='label+percent' , textinfo='value',
               textfont=dict(size=20),
               )
    data = go.Data([status_trace])
    layout = go.Layout(title='Activity Status',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
    fig = go.Figure(data=data,layout=layout)
    status_chart = plot(fig, output_type = 'div')

    #def plot_pie():


    return render(request , 'crm/index.html',
        {
            "contacts" : contacts,
            "organizations" : organizations,
            "teams_to_contacts" : teams_to_contacts,
            "activity_type_chart" : activity_type_chart,
            "status_chart" : status_chart,
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
    newsfeed = News.objects.all()
    return render(request, 'crm/newsfeed.html',{
                "newsfeed":newsfeed
            
    })