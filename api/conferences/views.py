from modularodm import Q
#from website.models import Conference, Node, Pointer
from website.models import Conference, Node
#from framework.auth.core import User
#from api.base import generic_bulk_views as bulk_views
#from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound
#from rest_framework.status import HTTP_204_NO_CONTENT
#from rest_framework.response import Response
#from framework.auth.oauth_scopes import CoreScopes
from api.base.views import JSONAPIBaseView
#from api.users.views import UserMixin
#from framework.auth.core import User
from api.base.filters import ODMFilterMixin


class ConferenceList(JSONAPIBaseView, ODMFilterMixin):
    model_class = Conference

    #serializer_class = ConferenceSerializer
    view_category = 'conference'
    view_name = 'conference-list'

    #def get_default_odm_query(self):
        #return (
            #Q('is_registered', 'eq', True)
        #)

    # overrides ListAPIView
    def get_queryset(self):
        query = self.get_query_from_request()
        print(Conference.find(query).get_keys())
        return Node.find(query)
