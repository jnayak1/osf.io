# -*- coding: utf-8 -*-

import bson
from modularodm import fields, Q
from modularodm.exceptions import ModularOdmException

from framework.mongo import StoredObject, ObjectId

from website.conferences.exceptions import ConferenceError
from website.project.model import Tag, Pointer

import datetime

DEFAULT_FIELD_NAMES = {
    'submission1': 'poster',
    'submission2': 'talk',
    'submission1_plural': 'posters',
    'submission2_plural': 'talks',
    'meeting_title_type': 'Posters & Talks',
    'add_submission': 'poster or talk',
    'mail_subject': 'Presentation title',
    'mail_message_body': 'Presentation abstract (if any)',
    'mail_attachment': 'Your presentation file (e.g., PowerPoint, PDF, etc.)'
}

class Conference(StoredObject):
    #: Determines the email address for submission and the OSF url
    # Example: If endpoint is spsp2014, then submission email will be
    # spsp2014-talk@osf.io or spsp2014-poster@osf.io and the OSF url will
    # be osf.io/view/spsp2014
    _id = fields.StringField(default=lambda: str(ObjectId()))
    endpoint = fields.StringField(primary=True, required=True, unique=True)
    #: Full name, e.g. "SPSP 2014"
    name = fields.StringField(required=True)
    info_url = fields.StringField(required=False, default=None)
    logo_url = fields.StringField(required=False, default=None)
    location = fields.StringField(required=False, default=None)
    start_date = fields.DateTimeField(default=None)
    end_date = fields.DateTimeField(default=None)
    submissionStartDate = fields.DateTimeField(default=None)
    submissionEndDate = fields.DateTimeField(default=None)
    reviewDeadlineDate = fields.DateTimeField(default=None)
    tags = fields.ForeignField('tag', list=True)
    sponsors = fields.ForeignField('conferenceSponsor', list=True, default=None)
    description = fields.StringField(required=True, default=None)
    dateCreated = fields.DateTimeField(default=datetime.datetime.now)
    dateModified = fields.DateTimeField(default=None)
    linkedNodes = fields.ForeignField('conference', list=True)
    permissions = fields.DictionaryField()
    pending = fields.BooleanField(default=True)
    declined = fields.BooleanField(default=False)
    active = fields.BooleanField(required=True)
    admins = fields.ForeignField('user', list=True, required=False, default=None)
    #: Whether to make submitted projects public
    public_projects = fields.BooleanField(required=False, default=True)
    poster = fields.BooleanField(default=True)
    talk = fields.BooleanField(default=True)
    # field_names are used to customize the text on the conference page, the categories
    # of submissions, and the email adress to send material to.
    field_names = fields.DictionaryField(default=lambda: DEFAULT_FIELD_NAMES)

    # Cached number of submissions
    num_submissions = fields.IntegerField(default=0)

    @classmethod
    def get_by_endpoint(cls, endpoint, active=True):
        query = Q('endpoint', 'iexact', endpoint)
        if active:
            query &= Q('active', 'eq', True)
        try:
            return Conference.find_one(query)
        except ModularOdmException:
            raise ConferenceError('Endpoint {0} not found'.format(endpoint))

    def add_permission(self, user, permission, save=False):
        """Grant permission to a user.

        :param User user: User to grant permission to
        :param str permission: Permission to grant
        :param bool save: Save changes
        :raises: ValueError if user already has permission
        """
        if user._id not in self.permissions:
            self.permissions[user._id] = [permission]
        else:
            if permission in self.permissions[user._id]:
                raise ValueError('User already has permission {0}'.format(permission))
            self.permissions[user._id].append(permission)
        if save:
            self.save()

    def remove_permission(self, user, permission, save=False):
        """Revoke permission from a user.

        :param User user: User to revoke permission from
        :param str permission: Permission to revoke
        :param bool save: Save changes
        :raises: ValueError if user does not have permission
        """
        try:
            self.permissions[user._id].remove(permission)
        except (KeyError, ValueError):
            raise ValueError('User does not have permission {0}'.format(permission))
        if save:
            self.save()

    def clear_permission(self, user, save=False):
        """Clear all permissions for a user.

        :param User user: User to revoke permission from
        :param bool save: Save changes
        :raises: ValueError if user not in permissions
        """
        try:
            self.permissions.pop(user._id)
        except KeyError:
            raise ValueError(
                'User {0} not in permissions list for node {1}'.format(
                    user._id, self._id,
                )
            )
        if save:
            self.save()

    def set_permissions(self, user, permissions, save=False):
        self.permissions[user._id] = permissions
        if save:
            self.save()

    def has_permission(self, user, permission):
        """Check whether user has permission.

        :param User user: User to test
        :param str permission: Required permission
        :returns: User has required permission
        """
        if user is None:
            return False
        if permission in self.permissions.get(user._id, []):
            return True
        if permission == 'read' and check_parent:
            return self.is_admin_parent(user)
        return False

    def get_permissions(self, user):
        """Get list of permissions for user.

        :param User user: User to check
        :returns: List of permissions
        :raises: ValueError if user not found in permissions
        """
        return self.permissions.get(user._id, [])

class ConferenceSubmission(Node):
    conference = fields.ForeignField('conference', required=True)


class ConferenceSponsor(StoredObject):
    _id = fields.StringField(default=lambda: str(ObjectId()))
    name = fields.StringField(required=True, default=None)
    logoURL = fields.StringField(required=False, default=None)

class MailRecord(StoredObject):
    _id = fields.StringField(primary=True, default=lambda: str(bson.ObjectId()))
    data = fields.DictionaryField()
    records = fields.AbstractForeignField(list=True)
