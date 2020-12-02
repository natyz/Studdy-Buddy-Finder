from django.contrib import messages
from django.db.models import ProtectedError, Q
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import UpdateView
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.views import generic
import html

from .forms import NewListingForm
from .models import Listing, UserProfile

import re

'''
/***************************************************************************************
*  REFERENCES
*  Title: Django QuerySet API Reference Documentation
*  Author: Django
*  Date: 10/15/20
*  Code version: 3.1
*  URL: https://docs.djangoproject.com/en/3.1/ref/models/querysets/
*  Software License:  3-clause BSD license
***************************************************************************************/
'''

class ListingsView(generic.CreateView):
    model = Listing
    template_name = 'listing/listing.html'
    fields = '__all__'

    def get_object(self, queryset=None):
        user = super(ListingsView, self).get_object(queryset)
        # Listing.objects.get(uid=user.username)
        return user


def listings_view(request):
    '''
    /***************************************************************************************
    Django QuerySet API Reference Documentation
    ***************************************************************************************/
    '''
    new_listing = Listing.get_all_listings.all()
    for n in new_listing:
        zid = UserProfile.objects.filter(username=request.user.username).filter(
            zoom_id__regex=r'\d+$')  # .values_list('zoom_id')
        # if zid:
        #     print("\n\n", zid, "\n\n")
        username = UserProfile.objects.filter(username=request.user.username)
        if request.user.username == n.uid and zid:
            n.zid = str(zid[0])
            n.save()
    context = {
        "new_listing": new_listing,
        "list": "study buddy listings",
        "grp_size": 1,
    }

    return render(request, "listing/listing.html", context)


def listings_table_view(request):
    new_listing = Listing.get_all_listings.all()
    context = {
        "new_listing": new_listing,
        "list": "study buddy listings",
    }

    return render(request, "listing/listing_table.html", context)


def users_listings_view(request):
    '''
    /***************************************************************************************
    Django QuerySet API Reference Documentation
    ***************************************************************************************/
    '''
    new_listing = Listing.cs_3240_listings.find_all_for(request.user.username)

    for n in new_listing:
        zid = UserProfile.objects.filter(username=request.user.username).filter(
            zoom_id__regex=r'\d+$')  # .values_list('zoom_id')
        # if zid:
        #     print("\n\n", zid, "\n\n")
        if request.user.username == n.uid and zid:
            n.zid = str(zid[0])
            n.save()
    context = {
        "new_listing": new_listing,
        "list": request.user.first_name.lower() + "slist",
        "grp_size": 1,
    }

    return render(request, "listing/mylistings.html", context)


def detail_view(request, id=None):
    listing = Listing.listings.filter(id=id)
    uid = Listing.listings.filter(Q(id=id)).values_list('uid')
    uid = re.sub(r"[(',)]+", '', str(uid[0]))
    context = {'listing': listing,
               'uid': uid,
               "grp_size": 1,
               }
    return render(request, 'listing/detail.html', context)


def save_listing_view(request, id=None):
    listing = Listing.listings.filter(id=id)
    uid = Listing.listings.filter(Q(id=id)).values_list('uid')
    uid = re.sub(r"[(',)]+", '', str(uid[0]))
    context = {'listing': listing,
               'uid': uid
               }
    return render(request, 'listing/profile.html', context)


def new_listing_form(request):
    zid = UserProfile.objects.filter(username=request.user.username).filter(
        zoom_id__regex=r'\d+$')  # .values_list('zoom_id')
    # print('\n\nZoomID: ', zid, '\n\n')
    if request.method == 'POST':
        f = NewListingForm(request.POST)
        # f = NewListingForm(request.POST, initial={'username': request.user.username})

        if f.is_valid():
            f.comment = f.cleaned_data['comment']
            # remember old state
            _mutable = f.data._mutable

            # set to mutable
            f.data._mutable = True

            # сhange the values you want
            f.initial['uid'] = request.user.first_name

            f.save()  # _m2m()

            # set mutable flag back
            f.data._mutable = _mutable
            # return HttpResponseRedirect(request.path_info, )

            return HttpResponseRedirect('/mylistings')
            # return HttpResponseRedirect(reverse('home:profile', kwargs={'slug': request.user}))  # render(request, 'profile/profile.html', {'object.userprofile': pro})  )

    else:
        f = NewListingForm()
    f.initial['uid'] = request.user.username
    if zid:
        print('\n\nif zid: ', str(zid[0]), '\n\n')
        context = {
            "f": f,
            'user_req': request.user.username
        }
    else:
        print('\n\nelse --> pro.zoomID: ', zid, '\n\n')

        context = {
            "f": f,
            'user_req': request.user.username,
            'zid': 'invalid'
        }
    return render(request, 'listing/create_listing.html', context)


def delete_listing(request, id=None):
    listing = get_object_or_404(Listing, id=id)
    # enlister = re.sub(r"@.*", '', listing.email)
    enlister = request.user.username

    if request.method == "POST" and request.user.is_authenticated:  # and request.user.username == enlister:
        try:
            listing.delete()
        except ProtectedError:
            error_message = "This listing can't be deleted!!"
            return JsonResponse(error_message)
        messages.success(request, "listing deleted.")

        return HttpResponseRedirect("/listings")

    context = {'listing': listing,
               'enlister': enlister,
               }

    return render(request, 'listing/delete.html', context)


def save_listing(request, id=None):
    listing = get_object_or_404(Listing, id=id)

    if request.method == "POST" and request.user.is_authenticated:  # and request.user.username == enlister:
        listing.save()
        messages.success(request, "listing saved.")
        return HttpResponseRedirect("/listings")

    context = {'listing': listing}

    return render(request, 'listing/save.html', context)


def join_group(request, id=None):
    listing = get_object_or_404(Listing, id=id)
    grp_cnt = 1
    if int(listing.num_members) > 1:
        if listing.member2 == 'vacant':
            listing.member2 = request.user.username
            grp_cnt = 2
        elif int(listing.num_members) > 2:
            if listing.member3 == "vacant" and listing.member2 != request.user.username:
                listing.member3 = request.user.username
                grp_cnt = 3
            elif int(listing.num_members) > 3:
                if listing.member4 == "vacant" and listing.member2 != request.user.username and listing.member3 != request.user.username:
                    listing.member4 = request.user.username
                    grp_cnt = 4
                elif int(listing.num_members) > 4:
                    if listing.member5 == "vacant" and listing.member2 != request.user.username and listing.member3 != request.user.username and listing.member4 != request.user.username:
                        listing.member5 = listing.uid
                        grp_cnt = 5
                else:
                    occupied = "sorry!  " + listing.uid + "'s group is at max capacity"
                    context = {'listing': listing, 'occupied': occupied}
                    return render(request, 'listing/save.html', context)
            else:
                occupied = "sorry!  " + listing.uid + "'s group is at max capacity"
                context = {'listing': listing, 'occupied': occupied}
                return render(request, 'listing/save.html', context)
        else:
            occupied = "sorry!  " + listing.uid + "'s group is at max capacity"
            context = {'listing': listing, 'occupied': occupied}
            return render(request, 'listing/save.html', context)
    else:
        occupied = "sorry!  " + listing.uid + "'s group is at max capacity"
        context = {'listing': listing, 'occupied': occupied}
        return render(request, 'listing/save.html', context)
    listing.save()
    context = {'listing': listing, 'member': listing.member2, 'grp_cnt': grp_cnt}
    return render(request, 'listing/save.html', context)


def leave_group(request, id=None):
    listing = get_object_or_404(Listing, id=id)
    grp_cnt = 1
    if listing.member5 == request.user.username:
        listing.member5 = "vacant"
        grp_cnt = 4
    elif listing.member4 == request.user.username:
        listing.member4 = "vacant"
        grp_cnt = 3
    elif listing.member3 == request.user.username:
        listing.member3 = "vacant"
        grp_cnt = 2
    elif listing.member2 == request.user.username:
        listing.member2 = "vacant"  # listing.uid
        grp_cnt = 1
    else:
        vacant = listing.uid + ", you are not a member of this group! "
        context = {'listing': listing, 'vacant': vacant}
        return render(request, 'listing/leave.html', context)
    listing.save()
    context = {'listing': listing, 'member': listing.member2, 'grp_cnt': grp_cnt, 'vacant': " sorry to see you go!"}
    return render(request, 'listing/leave.html', context)


def join_zoom(request, id=None):
    listing = get_object_or_404(Listing, id=id)
    zid = listing.zid
    # print('\n\nZoomID: ', zid, '\n\n')
    grp_cnt = 1
    context = {'listing': listing, 'member': listing.member2, 'grp_cnt': grp_cnt, 'zid': zid}
    return render(request, 'listing/zoom.html', context)


def edit_listing(request, id=None):
    listing_to_edit = get_object_or_404(Listing, id=id)
    if request.method == "POST" and request.user.is_authenticated:
        edit_form = NewListingForm(request.POST, instance=listing_to_edit)
        if edit_form.is_valid():
            _mutable = edit_form.data._mutable
            edit_form.data._mutable = True
            edit_form.initial['uid'] = request.user.username

            listing_to_edit = edit_form.save(commit=False)
            # listing_to_edit.save()
            edit_form.data._mutable = _mutable
            return redirect(request.path_info, 'listing/listing.html', id=listing_to_edit.id)

            # return redirect('post_detail', id=listing_to_edit.id)
    else:
        edit_form = NewListingForm(request.path_info, instance=listing_to_edit)
    return render(request, 'listing/create_listing.html', {'edit_form': edit_form})


def edit(request, id=None):
    instance = Listing.listings.filter(id=id)
    f = NewListingForm(request.POST or None, instance=instance)
    if f.is_valid():
        _mutable = f.data._mutable
        f.data._mutable = True
        f.initial['uid'] = request.user.username
        instance = f.save(commit=False)
        # listing_to_edit.save()
        f.data._mutable = _mutable
        return redirect(request.path_info, 'listing/listing.html', instance=instance)

        # return redirect('post_detail', id=listing_to_edit.id)
    else:
        f = NewListingForm(request.path_info, instance=instance)
    return render(request, 'listing/create_listing.html', {'f': f})


class EditListingView(UpdateView):
    model = Listing
    form_class = NewListingForm
    template_name = "listing/listing.html"

    def get_object(self, *args, **kwargs):
        # user = get_object_or_404(User, pk=self.kwargs['pk'])
        listing_to_edit = get_object_or_404(Listing, pk=self.kwargs['id'])

        return listing_to_edit.uid

    def get_success_url(self, *args, **kwargs):
        return reverse('/')


def listing_update(request, id):
    template_name = 'listing/listing.html'

    object = get_object_or_404(Listing, id=id)
    if request.method == 'POST':
        form = NewListingForm(instance=object, data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            if not request.is_ajax():
                # reload the page
                next = request.META['PATH_INFO']
                return HttpResponseRedirect(next)
            # if is_ajax(), we just return the validated form, so the modal will close
    else:
        form = NewListingForm(instance=object)

    return render(request, template_name, {
        'object': object,
        'form': form,
    })