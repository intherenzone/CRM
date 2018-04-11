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
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    this_user_object = User.objects.filter(username=username)[0]
    teamsObject_this_user_belongs_to = Team.objects.filter(members__username = this_user_object.username)
    contacts_lists_the_teams_have = []
    for team in teamsObject_this_user_belongs_to:
        contacts_the_team_has = Contact.objects.filter(teams__name = team.name)
        contacts_lists_the_teams_have.append(contacts_the_team_has)
    my_contactsObject_this_user_is_assigned_to = Contact.objects.filter(assigned_to__username=this_user_object.username)

    teamsObject_list_this_user_belongs_to = Team.objects.filter(members__username = this_user_object.username)
    teams_and_contacts_lists_the_teams_have = zip(teamsObject_list_this_user_belongs_to, contacts_lists_the_teams_have)

    #contacts_lists_the_teams_have = []
    #for i in range(len(teamsObject_this_user_belongs_to)):
    #    contacts_lists_the_teams_have.append([teamsObject_this_user_belongs_to[i]])
    #    contacts_the_team_has = Contact.objects.filter(teams__name = contacts_lists_the_teams_have[i][0])
    #    contacts_lists_the_teams_have[i].append([contacts_the_team_has])


    #count activity type
    act_type = []
    count_act_type = []
    for act in ACTIVITY_TYPE:
        act_type.append(act[0])
        count_act_type.append(Activity.objects.filter(activity_type = act[0]).count())

    trace = go.Pie(labels=act_type, values=count_act_type,
               hoverinfo='label+percent' , textinfo='value',
               textfont=dict(size=20),
               )

    act_type_chart = plot([trace], output_type = 'div')

    lead_status = []
    count_lead_status = []
    for lead in LEAD_STATUS:
        lead_status.append(lead[0])
        count_lead_status.append(Activity.objects.filter(status = lead[0]).count())

    lead_status_trace = go.Pie(labels=lead_status, values=count_lead_status,
               hoverinfo='label+percent' , textinfo='value',
               textfont=dict(size=20),
               )
    lead_status_chart = plot([lead_status_trace], output_type = 'div')

    #act_start_date = []
    #act_start_date_count = []
    #counter = Activity.objects.filter(startdate = lead[0]).count()
    #for act in

    #orgnization chart
    organizationsObjects_this_user_associated_with = Organization.objects.filter(assigned_to__username = this_user_object.username)



    return render(request , 'crm/index.html', {
    "teamsObject" : teamsObject_this_user_belongs_to,
    "my_contactsObjects" : my_contactsObject_this_user_is_assigned_to,
    "contacts_lists_the_teams_have" : contacts_lists_the_teams_have,
    #teamsObject_this_user_belongs_to : contacts_lists_the_teams_have,
    "teams_and_contacts_lists_the_teams_have" : teams_and_contacts_lists_the_teams_have,
    "act_type_chart" : act_type_chart,
    "lead_status_chart" : lead_status_chart,
    "my_organizationsObjects" : organizationsObjects_this_user_associated_with
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
