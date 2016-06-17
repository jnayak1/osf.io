from django.conf.urls import url
from api.conference import views

urlpatterns = [
        url(r'^$', views.ConferenceList.as_view(),
            name=views.ConferenceList.view_name),
        url(r'^(?P<conference_id>\w+)/$', views.ConferenceDetail.as_view(),
            name=views.ConferenceDetail.view_name),
        url(r'^(?P<conference_id>\w+)/submissions/$',
            views.SubmissionList.as_view(),
            name=views.SubmissionList.view_name),
        url(r'^(?P<conference_id>\w+)/submissions/(?P<submission_id>\w+)/',
            views.SubmissionDetail.as_view(),
            name=views.SubmissionDetail.view_name),
        url(r'^(?P<conference_id>\w+)/submissions/(?P<submission_id>\w+)/evaluation/$',
            views.SubmissionEval.as_view(),
            name=views.SubmissionEval.view_name),
        ]
