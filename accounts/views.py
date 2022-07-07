from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render,redirect
from post.models import Post
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .models import User, Connection, Mycommunity
from community.models import Community,CommunityPost
from django.views.generic import UpdateView


def user_profile(request, username):
    user_model = get_user_model().objects.get(username=username)
    context = {
        'User': user_model,
        'post_list': CommunityPost.objects.filter(author=user_model.id),
        'following': Connection.objects.filter(follower__username=username).count(),
        'follower': Connection.objects.filter(following__username=username).count(),
        'mycommunity': Mycommunity.objects.filter(follower__username=username).count(),
    }
    if username is not request.user.username:
            result = Connection.objects.filter(follower__username=request.user.username).filter(following__username=username)
            context['connected'] = True if result else False
    return render(request, 'accounts/user_profile.html', context)

class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser

class UserUpdateView(OnlyYouMixin, UpdateView):
    template_name = 'accounts/user_update.html'
    model = User
    fields = ('username', 'icon', 'introduction')

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'username': User.objects.get(pk=self.object.pk).username})

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

"""フォロー"""
@login_required
def follow_view(request, *args, **kwargs):

    try:
        #request.user.username = ログインユーザーのユーザー名を渡す。
        follower = User.objects.get(username=request.user.username)
        #kwargs['username'] = フォロー対象のユーザー名を渡す。
        following = User.objects.get(username=kwargs['username'])
    #例外処理：もしフォロー対象が存在しない場合、警告文を表示させる。
    except User.DoesNotExist:
        messages.warning(request, '{}は存在しません'.format(kwargs['username']))
        return HttpResponseRedirect(reverse_lazy('post:post_list'))
    #フォローしようとしている対象が自分の場合、警告文を表示させる。
    if follower == following:
        messages.warning(request, '自分自身はフォローできません')
    else:
        #フォロー対象をまだフォローしていなければ、DBにフォロワー(自分)×フォロー(相手)という組み合わせで登録する。
        #createdにはTrueが入る
        _, created = Connection.objects.get_or_create(follower=follower, following=following)

        #もしcreatedがTrueの場合、フォロー完了のメッセージを表示させる。
        if (created):
            messages.success(request, '{}をフォローしました'.format(following.username))
        #既にフォロー相手をフォローしていた場合、createdにはFalseが入る。
        #フォロー済みのメッセージを表示させる。
        else:
            messages.warning(request, 'あなたはすでに{}をフォローしています'.format(following.username))

    return HttpResponseRedirect(reverse_lazy('accounts:profile', kwargs={'username': following.username}))

"""フォロー解除"""
@login_required
def unfollow_view(request, *args, **kwargs):

    try:
        follower = User.objects.get(username=request.user.username)
        following = User.objects.get(username=kwargs['username'])
        if follower == following:
            messages.warning(request, '自分自身のフォローを外せません')
        else:
            unfollow = Connection.objects.get(follower=follower, following=following)
            #フォロワー(自分)×フォロー(相手)という組み合わせを削除する。
            unfollow.delete()
            messages.success(request, 'あなたは{}のフォローを外しました'.format(following.username))
    except User.DoesNotExist:
        messages.warning(request, '{}は存在しません'.format(kwargs['username']))
        return HttpResponseRedirect(reverse_lazy('post:post_list'))
    except Connection.DoesNotExist:
        messages.warning(request, 'あなたは{0}をフォローしませんでした'.format(following.username))

    return HttpResponseRedirect(reverse_lazy('accounts:profile', kwargs={'username': following.username}))

def following_list(request, username):
    context = {
        'username': username,
        'following': Connection.objects.filter(follower__username=username),
    }
    return render(request, 'accounts/following_list.html', context)

def follower_list(request, username):
    context = {
        'username': username,
        'follower': Connection.objects.filter(following__username=username),
    }
    return render(request, 'accounts/follower_list.html', context)

@login_required
def mycommunity_follow_view(request, comid):
    try:
        #request.user.username = ログインユーザーのユーザー名を渡す。
        follower = User.objects.get(username=request.user.username)
        #kwargs['username'] = フォロー対象のユーザー名を渡す。
        mycommunity = Community.objects.get(id=comid)
        #例外処理：もしフォロー対象が存在しない場合、警告文を表示させる。
    except Community.DoesNotExist:
        messages.warning(request, 'コミュニティーは存在しません')
        return HttpResponseRedirect(reverse_lazy('post:post_list'))
    #フォローしようとしている対象が自分の場合、警告文を表示させる。
    
    _, created = Mycommunity.objects.get_or_create(mycommunity=mycommunity, follower=follower)

        #もしcreatedがTrueの場合、フォロー完了のメッセージを表示させる。
    if (created):
        messages.success(request, '{}をフォローしました'.format(mycommunity.name))
        #既にフォロー相手をフォローしていた場合、createdにはFalseが入る。
        #フォロー済みのメッセージを表示させる。
    else:
        messages.warning(request, 'あなたはすでに{}をフォローしています'.format(mycommunity.name))
    
    community = Community.objects.get(id=comid)
    name = community.name
    return redirect('community:community_top', name=name)

"""フォロー解除"""
@login_required
def mycommunity_unfollow_view(request, comid):
    try:
        follower = User.objects.filter(username=request.user.username)
        mycommunity = Community.objects.filter(id=comid)
        Mycommunity.objects.all().delete()
        messages.success(request, 'あなたは{}のフォローを外しました'.format(mycommunity.name))
    except Community.DoesNotExist:
        messages.warning(request, 'コミュニティは存在しません')
        #return HttpResponseRedirect(reverse_lazy('post:post_list'))
    name = mycommunity.name
    return redirect('community:community_top', name=name)

def mycommunity_list(request, username):
    context = {
        'username': username,
        'mycommunity': Mycommunity.objects.filter(follower__username=username),
    }
    return render(request, 'accounts/mycommunity_list.html', context)