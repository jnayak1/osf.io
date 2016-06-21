# -*- coding: utf-8 -*-
from rest_framework import permissions
from rest_framework import exceptions

from website.models import Node, Pointer, User
from website.conferences.model import Conference, ConferenceSponsor
from website.project.metadata.utils import is_prereg_admin
from website.util import permissions as osf_permissions

from api.base.utils import get_user_auth
from admin.base.utils import OSFAdmin

class IsOSFAdmin(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		assert isinstance(obj, (Conference, Pointer, Node)), 'obj must be a Conference, Pointer or Node, got {}'.format(obj)
		return request.user.is_in_group('osf_admin')

class IsPublic(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		assert isinstance(obj, (Conference, Pointer, Node)), 'obj must be a Conference, Pointer or Node, got {}'.format(obj)
		return request.method in permissions.SAFE_METHODS

class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        assert isinstance(obj, (Conference, Pointer, Node)), 'obj must be a Conference, Pointer or Node got {}'.format(obj)
        auth = get_user_auth(request)
        if isinstance(obj, Conference)
        	return request.user in obj.admins
        if isinstance(obj, Pointer)
        	Conference.objects.filter(linkedNodes)
        	return 0
        # If admin for conference, return true

class CurrentOsfUser(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		assert isinstance(obj, (Conference, Pointer, Node)), 'obj must be a Conference, got {}'.format(obj)
		auth = get_user_auth(request)

class IsSubmissionContributor(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		assert isinstance(obj, (Conference, Pointer, Node)), 'obj must be a Conference, got {}'.format(obj)
		auth = get_user_auth(request)
		# If submission, and if submission author, PUT, DELETE, GET submission
		# else, like IsPublic
