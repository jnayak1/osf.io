# -*- coding: utf-8 -*-
from rest_framework import permissions
from rest_framework import exceptions

from website.models import Node, Pointer, User
from website.conferences.model import Conference, ConferenceSponsor, ConferenceSubmission
from website.project.metadata.utils import is_prereg_admin
from website.util import permissions as osf_permissions

from api.base.utils import get_user_auth
from admin.base.utils import OSFAdmin

class IsOSFAdmin(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		assert isinstance(obj, (Conference, ConferenceSubmission, Node)), 'obj must be a Conference, or Conference Submission, got {}'.format(obj)
		return request.user.is_in_group('osf_admin')

class IsPublic(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		assert isinstance(obj, (Conference, ConferenceSubmission)), 'obj must be a Conference, or ConferenceSubmission, got {}'.format(obj)
		return request.method in permissions.SAFE_METHODS

class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        assert isinstance(obj, (Conference, ConferenceSubmission)), 'obj must be a Conference, or ConferenceSubmission, got {}'.format(obj)
        auth = get_user_auth(request)
        if isinstance(obj, Conference)
        	return request.user in obj.admins
        if isinstance(obj, ConferenceSubmission)
        	return request.user in obj.conference.admins

class CurrentOsfUser(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		assert isinstance(obj, (Conference, Pointer)), 'obj must be a Conference, or ConferenceSubmission, got {}'.format(obj)
		auth = get_user_auth(request)
		if request.method in permissions.SAFE_METHODS:
			return True
		# TODO: POST methods

class IsSubmissionContributor(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		assert isinstance(obj, (Conference, Pointer, Node)), 'obj must be a Conference, or ConferenceSubmission, got {}'.format(obj)
		auth = get_user_auth(request)
		# If submission, and if submission author, PUT, DELETE, GET submission
		# else, like IsPublic



# Conference List
# A conference detail
# 	A conference submission list
# 	A conference submission detail
# 		A conference submission’s evaluation list
# 		A conference submission’s evaluation detail

# GET a conference
# GET a conference list
# POST a conference
# DELETE a conference
# PUT a conference
# 	Edit information about a conference
# **create wrapper for submission since a submission is a pointer** (talk to Jeff)
# GET a submission
# GET a submission list
# POST a submission
# PUT a submission
# 	Approve a submission to a conference
# 	Reject a submission to a conference
# DELETE a submission
# GET a submission evaluation on a submission
# GET submission evaluation list
# POST a submission evaluation on a submission
# PUT a submission evaluation on a submission
# DELETE a submission evaluation on a submission

# IsOSFAdmin
# 	-GOD
# isAdmin
# 	- All actions on and relating to their conference
# isPublic
# 	-GET a conference
# 	-GET conference list
# -GET a submission
# Approved submission only
# 	-GET submission list
# Approved submissions
# CurrentOsfUser
# 	-GET conference list
# 	-GET conference
# 	-POST a conference
# 	-POST a submission
# 	-GET submission
# Approved submissions
# 	-GET submission list
# Approved submissions
# 	-POST a submission evaluation
# IsSubmissionContributor
# 	-PUT a submission
# Edit without changing submission status
# 	-DELETE a submission
# 	-GET submission
# currentUser submission and approved submissions
# 	-GET submission list
# currentUser submissions and approved submissions









