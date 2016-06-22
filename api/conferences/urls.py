from django.conf.urls import url
from api.conferences import views

urlpatterns = [

    #List of conferences
    url(r'^$', views.ConferenceList.as_view(), name=views.ConferenceList.view_name),

    #Detail a conference
    #url(r'^(?P<conference_id>\w+)/$', views.ConferenceDetail.as_view(),
        #name=views.ConferenceDetail.view_name),

    #List of submissions to a conference
    #url(r'^(?P<conference_id>\w+)/submissions/$',
        #views.SubmissionList.as_view(),
        #name=views.SubmissionList.view_name),

    #Detail of a submission to a conference
    #url(r'^(?P<conference_id>\w+)/submissions/(?P<submission_id>\w+)/$',
        #views.SubmissionDetail.as_view(),
        #name=views.SubmissionDetail.view_name),

    #Detail of a submission's evaluation
    #url(r'^(?P<conference_id>\w+)/submissions/(?P<submission_id>\w+)/evaluation/$',
        #views.SubmissionEval.as_view(), name=views.SubmissionEval.view_name),

]
