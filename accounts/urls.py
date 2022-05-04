from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/<str:username>/', views.user_profile, name='profile'),
    path('profile/<str:username>/follow', views.follow_view, name='follow'),
    path('profile/<str:username>/unfollow', views.unfollow_view, name='unfollow'),
    path('profile/<str:username>/following_list', views.following_list, name='following_list'),
    path('profile/<str:username>/follower_list', views.follower_list, name='follower_list'),
    path('profile/update/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),
]
