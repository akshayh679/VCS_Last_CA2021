from django.urls import path
from .views import home, signup, login, get_all_users, get_user_by_email,update_user,delete_user

urlpatterns = [
    path('', home),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('users/', get_all_users, name='get_all_users'),
    path('user/', get_user_by_email, name='get_user_by_email'),
    path('update/', update_user, name='update_user'),
    path('delete/', delete_user, name='delete_user'),
]
