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
    status = ['in process', 'converted', 'recycled', 'assigned', 'dead']
    activity_obj = sorted(Activity.objects.all().order_by('enddate', 'startdate'), key=lambda p: status.index(p.status))

    page = request.POST.get('per_page')

    # email = request.POST.get('email')
    # if email:
    # activity_obj = Activity.objects.filter(email__icontains=email)

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
            #activity_obj.contacts.add(*contacts_list)
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

@login_required
def remove_activity(request, pk):
    activity_record = get_object_or_404(Activity, id=pk)
    activity_record.delete()
    if request.is_ajax():
        return JsonResponse({'error': False})
    else:
        return HttpResponseRedirect(reverse('activities:list'))



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
            #activity_obj.contacts.add(*contacts_list)
            if request.is_ajax():
                return JsonResponse({'error': False})
            return HttpResponseRedirect(reverse('activities:list'))
        else:
            print(form.errors)
            if request.is_ajax():
                return JsonResponse({'error': True, 'activity_errors': form.errors})
            return render(request, 'activity/create_activity.html', {
                          'activity_form': form,
                          'activity_obj': activity_obj,
                          'users': users,
                          'assignedto_list': assignedto_list,
                          'contacts_list': contacts_list
                    })
    else:
        return render(request, 'activity/create_activity.html', {
                      'activity_form': form,
                      'activity_obj': activity_obj,
                      'users': users,
                      'assignedto_list': assignedto_list,
                      'contacts_list': contacts_list
                })

@login_required
def view_activity(request, pk):
    activity_record = get_object_or_404(
        Activity, id=pk)
    #comments = activity_record.activity_comments.all()
    return render(request, 'activity/view_activity.html', {
        'activity_record': activity_record})
#'comments': comments



#Comment

@login_required
def add_comment(request):
    if request.method == 'POST':
        activity = get_object_or_404(Activity, id=request.POST.get('activityid'))
        if request.user in activity.assigned_to.all():
            form = ActivityCommentForm(request.POST)
            if form.is_valid():
                activity_comment = form.save(commit=False)
                activity_comment.comment = request.POST.get('comment')
                activity_comment.commented_by = request.user
                activity_comment.contact = contact
                activity_comment.save()
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









