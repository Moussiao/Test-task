from django.urls import path

from .views import StrangePostsHome, GetUser, ShowPost, UserPostsDynamicLoad

urlpatterns = [
    path('', StrangePostsHome.as_view(), name='home'),
    path('users/id<int:pk>', GetUser.as_view(), name='get_user'),
    path('load-more-posts/', UserPostsDynamicLoad.as_view(), name='load_more_posts'),
    path('post/<int:pk>', ShowPost.as_view(), name='post'),
]
