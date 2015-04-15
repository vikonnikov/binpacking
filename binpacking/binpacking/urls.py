from django.conf.urls import include, url
from django.contrib import admin
from packer.views import IndexPageView, pack

urlpatterns = [
    # Examples:
    # url(r'^$', 'binpacking.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', IndexPageView.as_view()),
    url(r'^pack/', pack),
]
