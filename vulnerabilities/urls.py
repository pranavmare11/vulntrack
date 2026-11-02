from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path(
        'reset-password/<uidb64>/<token>/',
        views.reset_password,
        name='reset-password',
    ),
    path('profile/', views.profile, name='profile'),
    path('create-post/', views.create_post, name='create_post'),
    path('explore/', views.explore, name='explore'),

    # Individual post detail page
    path(
        'explore/<int:pk>/',
        views.post_detail,
        name='post_detail',
    ),

    # Like and dislike actions
    path(
        'post/<int:pk>/react/<str:action>/',
        views.react,
        name='react',
    ),

    path('regisert_user/', views.regisert_user, name='regisert_user'),
    path('my_finding/', views.my_finding, name='my_finding'),
]