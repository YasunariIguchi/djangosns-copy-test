from django.shortcuts import get_object_or_404, render, redirect
from .forms import PostCreateForm
from .models import Post
from community.models import Community
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import SignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import(LoginView, LogoutView)
from .forms import LoginForm
from community.models import Community
import folium
from folium import plugins
import branca


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html" 
    success_url = reverse_lazy('post:post_list')

    def form_valid(self, form):
        user = form.save() # formの情報を保存
        login(self.request, user) # 認証
        self.object = user 
        return HttpResponseRedirect(self.get_success_url()) # リダイレクト

# Create your views here.


def post_list(request):
    counter = 0
    size = Post.objects.all().count()
    for counter in range(size):
        counter = counter +1
        comment = Post.objects.filter(id=counter).first()
        comment.display = 0
        comment.save()
    
    counter = 0
    cid = None

    while not Post.objects.filter(display=0).first() is None:
        comment = Post.objects.filter(parent_id=cid,display=0).first()
        if comment is None:
            counter = counter
            comment = Post.objects.filter(id=cid).first()
            cid = comment.parent_id
        else:
            counter = counter + 1
            comment.display = counter
            comment.save()
            cid = comment.id
    counter = 0

    size = Community.objects.all().count()
    map = folium.Map(location=[34.700559, 135.495734], zoom_start=15)
    if Community.objects.first() is None:
        x = 135.495734
        y = 34.700559
        url = request._current_scheme_host+'/community/community_create'
        html = '<a href = "'+ url +'" target="_blank" rel="noopener noreferrer">コミュニティを作る</a>'
        iframe = branca.element.IFrame(html=html, width=300, height=500)
        popup = folium.Popup(iframe, max_width=300)
        map = folium.Map(location=[y, x], zoom_start=15)
        folium.Marker(
        location=[y, x],
        popup = popup,
        icon=folium.Icon(color='red', icon='home')
        ).add_to(map)
    else:
        for l in Community.objects.all():
            name = l.name
            x = l.lon
            y = l.lat
            url = request._current_scheme_host+'/community/community_top/' + str(name) + '/'
            html = '<a href = "'+url + '" target="_blank" rel="noopener noreferrer">' + str(name) + '</a>'
            iframe = branca.element.IFrame(html=html, width=300, height=500)
            popup = folium.Popup(iframe, max_width=300)
            folium.Marker(
            location=[y, x],
            popup = popup,
            icon=folium.Icon(color='red', icon='home')
            ).add_to(map)
    plugins.LocateControl(auto_start=False).add_to(map)
    map = map._repr_html_()


    context = {
        'post_list': Post.objects.order_by("display"),
        'reply_list': Post.objects.filter(parent__isnull=True),
        'community_list': Community.objects.all(),
        'map': map

    }
    return render(request, 'post/post_list.html', context)


def post_create(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post:post_list')
    else:
        form = PostCreateForm()
    return render(request, 'post/post_create.html', {'form': form})

class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'accounts/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'accounts/login.html'

def reply_create(request,comment_pk):
    comment = get_object_or_404(Post, id=comment_pk)
    post = comment
    form = PostCreateForm(request.POST or None)
    if request.method == 'POST':
        reply = form.save(commit=False)
        reply.parent = post
        reply.author = request.user
        reply.save()
        return redirect('post:post_list')

    context = {
        'form': form,
        'post': post,
        'comment': comment,
    }
    return render(request, 'post/post_create.html', context)
