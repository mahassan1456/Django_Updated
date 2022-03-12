
from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', view=views.vote, name='vote'),
    path('login/', view=views.login_user, name='login_user'),
    path('success/', view=views.success, name="success"),
    path('logout_user/', view=views.logout_user, name='logout_user'),
    path('signup/', views.sign_up, name='sign_up'),
    path('add_question/', views.add_question, name='add_question'),
    path('<int:question_id>/edit_question/', views.edit, name='edit'),
    path('view_profile/<int:user_id>/', views.view_profile, name="view_profile"),
    path('add_friend/<int:user_id>', views.add_friend, name='add_friend'),
    path('friend_requests/', views.view_requests, name='view_requests'),
    path('accept_requests/<int:user_id>/', views.accept_request, name='accept_request'),
    path('remove_friend/<int:user_id>/', views.remove_friend, name='remove_friend'),
    path('cancel_request/<int:user_id>/', views.cancel_request, name='cancel_request'),
    path('comments/<int:user_id>/', views.make_comment, name='make_comment'),
    path('chart/<int:question_id>', view=views.chart, name='chart'),
    path('search/', views.UserList.as_view(), name='search'),
    path('profile_settings/', view=views.profile_settings, name='profile_settings'),
    path('test123/', views.test123, name='test123')
]