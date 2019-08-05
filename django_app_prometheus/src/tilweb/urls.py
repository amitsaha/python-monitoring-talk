from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^me/', views.me, name='me'),
    url(r'^post/$', views.create_post, name='create-post'),
    url(r'^post/(?P<post_id>\d+)/$', views.show_post, name='show-post'),
    url(r'^tag/(?P<tag>\w+)/$', views.tag_view, name='tag-view'),
    url(r'^signup/$', views.signup, name='signup'),
]
