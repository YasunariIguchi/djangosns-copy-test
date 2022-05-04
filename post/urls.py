from django.urls import path
from . import views


app_name = 'post'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post_create/', views.post_create, name='post_create'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('index/', views.index, name='index'),
    path('ajax/', views.call_write_data, name='call_write_data'),
    path('include/reply/<int:comment_pk>/', views.reply_create, name='reply_create')
]

