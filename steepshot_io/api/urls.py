from django.conf.urls import url, include

from steepshot_io.api import views

urlpatterns = [
    url(r'^v1/', include([
        url(r'^work-request$', views.WorkRequestAPIView.as_view(), name='work_request'),
        url(r'^request$', views.RequestAPIView.as_view(), name='request'),
    ]), name='api_v1'),
]
