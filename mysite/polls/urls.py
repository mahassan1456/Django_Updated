
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
    path('signup/', views.sign_up, name='sign_up')
]