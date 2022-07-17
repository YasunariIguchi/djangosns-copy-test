from ast import IsNot
from django.shortcuts import get_object_or_404, render,render, redirect
from .forms import CommunityCreateForm, CommunityPostCreateForm
from .models import Community, CommunityPost
from accounts.models import Mycommunity, User
import requests
from bs4 import BeautifulSoup

# Create your views here.

geocoding_URL = 'http://www.geocoding.jp/api/'

def coordinate(address):
    """
    addressに住所を指定すると緯度経度を返す。

    >>> coordinate('東京都文京区本郷7-3-1')
    ['35.712056', '139.762775']
    """
    payload = {'q': address}
    html = requests.get(geocoding_URL, params=payload)
    soup = BeautifulSoup(html.content, "html.parser")
    if soup.find('error'):
        raise ValueError(f"Invalid address submitted. {address}")
    latitude = float(soup.find('lat').string)
    longitude = float(soup.find('lng').string)
    return [latitude, longitude]


def community_create(request):
    if request.method == "POST":
        form = CommunityCreateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            memo = form.cleaned_data["memo"]
            zip21 = form.cleaned_data["zip21"]
            zip22 = form.cleaned_data["zip22"]
            addr21 = form.cleaned_data["addr21"]
            lat, lon = coordinate(addr21)
            obj = Community(name=name, memo=memo, created_by = request.user, lat = lat, lon = lon, zip21 =zip21, zip22=zip22, addr21=addr21)
            obj.save()
            return redirect('post:post_list')
    else:
        form = CommunityCreateForm()
    return render(request, 'community/community_create.html', {'form': form})

def community_top(request, name):
    community = Community.objects.get(name=name)
    if request.method == "POST":
        form = CommunityPostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.community = community
            post.save()
            return redirect('community:community_top', name=name)
    else:
        form = CommunityPostCreateForm()
    
    counter = 0 
    counter = 1
    size = CommunityPost.objects.all().count()
    for counter in range(size):
        if CommunityPost.objects.filter(community=community,id=counter).first() is None:
            counter = counter
        else:
            comment = CommunityPost.objects.filter(community=community,id=counter).first()
            comment.display = 0
            comment.save()
    
    counter = 0
    cid = None

    while not CommunityPost.objects.filter(community=community,display=0).first() is None:
        comment = CommunityPost.objects.filter(community=community,parent_id=cid,display=0).first()
        if comment is None:
            counter = counter
            comment = CommunityPost.objects.filter(community=community,id=cid).first()
            cid = comment.parent_id
        else:
            counter = counter + 1
            comment.display = counter
            comment.save()
            cid = comment.id
    
    communitypost=CommunityPost.objects.filter(community=community).order_by("display")
    mycommunity = Mycommunity.objects.filter(mycommunity=community,follower=request.user).count()
    s=mycommunity
    return render(request, 'community/community_top.html', {'form': form, 'Community': community, 'CommunityPost': communitypost, 'mycommunity':s})

def reply_create(request,comment_pk,name):
    community = Community.objects.get(name=name)
    comment = CommunityPost.objects.filter(community=community,id=comment_pk).first()
    post = comment
    form = CommunityPostCreateForm(request.POST or None)
    if request.method == 'POST':
        reply = form.save(commit=False)
        reply.parent = post
        reply.community = community
        reply.author = request.user
        reply.save()
        return redirect('community:community_top', name=name)

    context = {
        'form': form,
        'post': post,
        'comment': comment,
    }
    return render(request, 'community/reply_create.html', context)