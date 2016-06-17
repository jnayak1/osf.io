# -*- coding: utf-8 -*-
from rest_framework import permissions
from rest_framework import exceptions

from website.models import Node, Pointer, User
from website.conferences.model import Conference, ConferenceSponsor
from website.project.metadata.utils import is_prereg_admin
from website.util import permissions as osf_permissions

from api.base.utils import get_user_auth

class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        assert isinstance(obj, Conference), 'obj must be a Conference, got {}'.format(obj)
        auth = get_user_auth(request)
        node = Node.load(request.parser_context['kwargs']['node_id'])
        return node.has_permission(auth.user, osf_permissions.ADMIN)

class AdminOrPublic(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        assert isinstance(obj, Conference), 'obj must be a Node, User, Institution, or Draft Registration, got {}'.format(obj)
        auth = get_user_auth(request)
        conference = Conference.load(request.parser_context['kwargs'][view.node_lookup_url_kwarg])
        if request.method in permissions.SAFE_METHODS:
            return node.is_public or node.can_view(auth)
        else:
            return node.has_permission(auth.user, osf_permissions.ADMIN)