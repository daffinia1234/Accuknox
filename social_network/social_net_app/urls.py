from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.Login,name="login"),
    path('signup/',views.Signup,name="signup"),
    path('logout/',views.Logout,name="logout"),
    path('search/', views.UserSearchView.as_view(), name='user-search'),
]