from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.Login,name="login"),
    path('signup/',views.Signup,name="signup"),
    path('logout/',views.Logout,name="logout"),
    path('search/', views.UserSearchView.as_view(), name='user-search'),
    path('sendrequest/<int:userID>/',views.send_request,name='send-friend-request'),
    path('openrequests/',views.get_open_request,name='open-requests'),
    path('accept/<int:requestID>/',views.accept,name='accept'),
]