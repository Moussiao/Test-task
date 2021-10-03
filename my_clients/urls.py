from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('sign_up/', views.RegisterUser.as_view(), name='sign_up'),
    path('logout/', views.logout_user, name='logout'),
    # path('id<int:pk>', views.GetUser.as_view(), name='get_user'),
]
