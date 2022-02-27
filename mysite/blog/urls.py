from django.urls import path

from . import views


app_name = 'blog'

urlpatterns = [

    path('<int:pk>/<slug:slug>/', view=views.ArticleView.as_view(), name='article'),
    path('', view=views.AllPosts.as_view(), name='all_posts'),
    path('create/', view=views.MakePost.as_view(), name='make_post'),
    path('comment/<int:article_id>', views.post_comment, name='post_comment')

]