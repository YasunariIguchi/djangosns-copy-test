from ast import IsNot
from django.shortcuts import get_object_or_404, render,render, redirect
from .forms import CommunityCreateForm, CommunityPostCreateForm
from .models import Community, CommunityPost

# Create your views here.


def community_create(request):
    if request.method == "POST":
        form = CommunityCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
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

    return render(request, 'community/community_top.html', {'form': form, 'Community': community, 'CommunityPost': CommunityPost.objects.filter(community=community).order_by("display")})

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