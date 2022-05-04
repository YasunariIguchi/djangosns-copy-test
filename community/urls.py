from django.urls import path
from . import views


app_name = 'community'

urlpatterns = [
    path('community_create/', views.community_create, name='community_create'),
    path('community_top/<str:name>/', views.community_top, name='community_top'),
    path('include/reply/<int:comment_pk>/<str:name>', views.reply_create, name='reply_create')
]