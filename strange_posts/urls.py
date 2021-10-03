from django.urls import path

from . import views

urlpatterns = [
    path('', views.StrangePostsHome.as_view(), name='home'),
    path('load-more-posts/', views.UserPostsDynamicLoad.as_view(), name='load_more_posts'),
    path('users/id<int:pk>', views.GetUser.as_view(), name='get_user'),
    path('post/<int:pk>', views.ShowPost.as_view(), name='post'),
]
