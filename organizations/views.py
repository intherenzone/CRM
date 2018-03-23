from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from common.models import Address, Comment, Team
from common.forms import BillingAddressForm
from common.utils import LEAD_STATUS, LEAD_SOURCE, COUNTRIES
from organizations.models import Organization
from organizations.forms import OrganizationForm, OrganizationCommentForm

from django.contrib.auth.models import User
from django.conf import settings


# CRUD Operations Start


@login_required
def organizations_list(request):
    org_obj = Organization.objects.all()
    page = request.POST.get('per_page')
    name = request.POST.get('name')
    city = request.POST.get('city')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
#    source= request.POST.get('lead_source')

    if name:
        org_obj = Organization.objects.filter(name__icontains=name)
    if city:
        a = Address.objects.filter(city__icontains=city)
        org_obj = Organization.objects.filter(address__in=a)
    if phone:
        org_obj = Organization.objects.filter(phone__icontains=phone)
    if email:
        org_obj = Organization.objects.filter(email__icontains=email)
#    if source:
#        org_obj = Organization.objects.filter(source__icontains=source)


    return render(request, 'crm/organizations/organizations.html', {
        'org_obj': org_obj,
        'per_page': page
#        'sources': LEAD_SOURCE,
    })


@login_required
def add_organization(request):
    users = User.objects.filter(is_active=True).order_by('email')
    form = OrganizationForm(assigned_to=users)
    address_form = BillingAddressForm()
    teams = Team.objects.all()
    assignedto_list = request.POST.getlist('assigned_to')
    teams_list = request.POST.getlist('teams')
    if request.method == 'POST':
        form = OrganizationForm(request.POST, assigned_to=users)
        address_form = BillingAddressForm(request.POST)
        if form.is_valid() and address_form.is_valid():
            address_obj = address_form.save()
            org_obj = form.save(commit=False)
            org_obj.address = address_obj
            org_obj.created_by = request.user
            org_obj.save()
            org_obj.assigned_to.add(*assignedto_list)
            org_obj.teams.add(*teams_list)
            if request.is_ajax():
                return JsonResponse({'error': False})
            if request.POST.get("savenewform"):
                return HttpResponseRedirect(reverse("organizations:add_organization"))
            else:
                return HttpResponseRedirect(reverse('organizations:list'))
        else:
            if request.is_ajax():
                return JsonResponse({'error': True, 'organization_errors': form.errors})
            return render(request, 'crm/organizations/create_organization.html', {
                          'organization_form': form,
                          'address_form': address_form,
                          'users': users,
                          'source': LEAD_SOURCE,
                          'teams': teams,
                          'assignedto_list': assignedto_list,
                          'teams_list': teams_list
            })
    else:
        return render(request, 'crm/organizations/create_organization.html', {
                      'organization_form': form,
                      'address_form': address_form,
                      'users': users,
                      'source': LEAD_SOURCE,
                      'teams': teams,
                      'assignedto_list': assignedto_list,
                      'teams_list': teams_list
        })


@login_required
def view_organization(request, organization_id):
    organization_record = get_object_or_404(Organization, id=organization_id)
    comments = organization_record.organization_comments.all()
    return render(request, 'crm/organizations/view_organization.html', {
        'organization_record': organization_record,
        'comments': comments})


@login_required
def edit_organization(request, pk):
    org_obj = get_object_or_404(Organization, id=pk)
    address_obj = get_object_or_404(Address, id=org_obj.address.id)
    users = User.objects.filter(is_active=True).order_by('email')
    form = OrganizationForm(
        instance=org_obj,assigned_to=users)
    address_form = BillingAddressForm(instance=address_obj)
    teams = Team.objects.all()
    assignedto_list = request.POST.getlist('assigned_to')
    teams_list = request.POST.getlist('teams')
    if request.method == 'POST':
        form = OrganizationForm(
            request.POST, instance=org_obj,assigned_to=users)
        address_form = BillingAddressForm(request.POST, instance=address_obj)
        if  form.is_valid() and address_form.is_valid():
            address_obj = address_form.save()
            org_obj = form.save(commit=False)
            org_obj.address = address_obj
            org_obj.created_by = request.user
            if request.POST.get('stage') in ['CLOSED WON', 'CLOSED LOST']:
                org_obj.closed_by = request.user
                org_obj.save()
                org_obj.assigned_to.clear()
                org_obj.assigned_to.add(*assignedto_list)
                org_obj.teams.clear()
                org_obj.teams.add(*teams_list)
            if request.is_ajax():
                return JsonResponse({'error': False})
            return HttpResponseRedirect(reverse('organizations:list'))
        else:
            if request.is_ajax():
                return JsonResponse({'error': True, 'organization_errors': form.errors})
            return render(request, 'crm/organizations/create_organization.html', {
                'organization_form': form,
                'address_form': address_form,
                'org_obj': org_obj,
                'teams': teams,
                'users': users,
                'assignedto_list': assignedto_list,
                'teams_list': teams_list

            })
    else:
        return render(request, 'crm/organizations/create_organization.html', {
                'organization_form': form,
                'address_form': address_form,
                'org_obj': org_obj,
                'teams': teams,
                'users': users,
                'assignedto_list': assignedto_list,
                'teams_list': teams_list
        })


@login_required
def remove_organization(request, pk):
    organization_record = get_object_or_404(Organization, id=pk)
    organization_record.delete()
    if request.is_ajax():
        return JsonResponse({'error': False})
    else:
        return HttpResponseRedirect(reverse('organizations:list'))

# CRUD Operations Ends
# Comments Section Starts


@login_required
def add_comment(request):
    if request.method == 'POST':
        organization = get_object_or_404(Organization, id=request.POST.get('organizationid'))
        if request.user in organization.assigned_to.all() or request.user == organization.created_by:
            form = OrganizationCommentForm(request.POST)
            if form.is_valid():
                organization_comment = form.save(commit=False)
                organization_comment.comment = request.POST.get('comment')
                organization_comment.commented_by = request.user
                organization_comment.organization = organization
                organization_comment.save()
                data = {"comment_id": organization_comment.id,"comment": organization_comment.comment,
                        "commented_on": organization_comment.commented_on,
                        "commented_by": organization_comment.commented_by.email}
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
        form = OrganizationCommentForm(request.POST)
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

# Other Views


@login_required
def get_organizations(request):
    if request.method == 'GET':
        organizations = Organization.objects.filter()
        return render(request, 'crm/organizations/organizations_list.html', {'organizations': organizations})
    else:
        return HttpResponse('Invalid Method or Not Authenticated in load_calls')
