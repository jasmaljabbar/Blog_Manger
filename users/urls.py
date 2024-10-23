from django.urls import path
from users import views

app_name = "users"

urlpatterns = [
    path("register/", views.UserRegisterationAPIView.as_view(), name="create-user"),
    path('login/', views.UserLoginAPIView.as_view(), name='login'),
    path('auth/logout/', views.UserLogoutAPIView.as_view(), name='logout'),
    path('auth/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path("", views.UserAPIView.as_view(), name="user-info"),
    path("profile/", views.UserProfileAPIView.as_view(), name="user-profile"),
    path("profile/avatar/", views.UserAvatarAPIView.as_view(), name="user-avatar"),
]

