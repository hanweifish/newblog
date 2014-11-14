from django.conf.urls import patterns, include, url
from newblog import views
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # ex: /polls/
    url(r'^$', views.blog_index, name='blog_index'),
    url(r'^(?P<blog_id>\d+)/$', views.blog_detail, name='blog_detail'),
    # url(r'^tag/(?P<blog_id>\d+)/$', views.blog_filter, name='blog_filter'),
    url(r'^add/$', views.blog_add, name='blog_add'),
    url(r'^(?P<blog_id>\d+)/update/$', views.blog_update, name='blog_update'),
    url(r'^(?P<blog_id>\d+)/del/$', views.blog_del, name='blog_del'),
    url(r'^login/$',  views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^profile/$', views.profile, name='blog_profile'),
    url(r'^myblog/$',  views.myblog, name='blog_myblog'),
    url(r'^tag/(?P<id>\d+)/$', views.blog_filter, name='blog_filter'),
    # url(r'^(?P<blog_id>\d+)/commentshow/$', views.blog_show_comment, name='showcomment'),
    # url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
    # url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
    # url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
)