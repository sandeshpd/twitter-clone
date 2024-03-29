from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('search_user/', views.search_user, name='search_user'),
    path('profile/followers/<int:pk>', views.followers, name='followers'),
    path('profile/follows/<int:pk>', views.follows, name='follows'),
    path('login/', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('signup/', views.signup_user, name='signup'),
    path('update/', views.update_user, name='update'),
    path('tweet_like/<int:pk>', views.tweet_like, name='tweet_like'),
    path('tweet/<int:pk>/comment/', views.tweet_comment, name='tweet_comment'),
    path('tweet_share/<int:pk>', views.tweet_share, name='tweet_share'),
    path('tweet_delete/<int:pk>', views.tweet_delete, name='tweet_delete'),
    path('bookmark/<int:pk>', views.save_bookmark_tweet, name='save_bookmark'),
    path('tweet_bookmark/', views.show_bookmark_tweet, name='tweet_bookmark'),
    path('unfollow/<int:pk>', views.unfollow, name='unfollow'),
    path('follow/<int:pk>', views.follow, name='follow'),
]