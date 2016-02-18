
# Copyright 2013 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
/rebac endpoint for Rebac API
"""

import copy
import eventlet
from oslo_config import cfg
import oslo_log.log as logging
import uuid

from rebac.common import wsgi
from rebac.common import exception
from rebac.i18n import _
from rebac.db import sql
from rebac.api import policy


CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class Controller(object):
    """
    WSGI controller for Policy Decision Point in Rebac API

    The PDP resource API is a RESTful web service for Policy Decisions. The API
    is as follows::

        POST /check -- check the Policy Decision
        POST /enforce -- check the Policy Decision to be enforced
    """

    # User CRUD
    def __init__(self):
      self.ACL = sql.ACLOperation()
      self.relationship = sql.RelationshipOperation()

    def user_authorized(self, req):
      #user = req.user
      #target_file = req.file
      # logic to check if user is allowed to access the file
      # If allowed then return true
      return False
       

    def create_relationship(self, req):

     sourcefile = {} 
     sourcefile['cloudname'] = 'c1'
     sourcefile['accountname'] = 'a1'
     sourcefile['containername'] = 'con1'
     sourcefile['filename'] = 'a1'

     targetfilelist = {}
     targetfilelist['cloudname']= 'tc1'
     targetfilelist['accountname']='ta1'
     targetfilelist['containername']= 'tcon1'
     targetfilelist['filename'] ='tf1'

     relationship ={}
     relationship['id'] = uuid.uuid4().hex
     relationship['sourcefile']= str(sourcefile)
     relationship['targetfilelist']= str(targetfilelist)

     return relationship.create_relationship(relationship['id'],relationship)

    def get_relationship(self, sourceFilename):
      ref = relationship.get_relationship(sourcefilename)
      return ref

    # Test this
    def create_object_acl(self, req, body):

     print("My Req is --> ", req)
     print("My Req is --> ", body)

     sourcefile = {}
     sourcefile['cloudname'] = body['sourcefile']['acl']
     sourcefile['accountname'] = 
     sourcefile['containername'] = 
     sourcefile['filename'] = "a1"

     userlist = {}
     userlist['cloudname']= "tuc1"
     userlist['accountname']="tua1"
     userlist['containername']= "ucon1"
     userlist['user_id'] ="tf1"
    
     acl = {}
     acl['id'] = uuid.uuid4().hex
     acl['sourcefile']= str(sourcefile)
     acl['userlist']= str(userlist)

     print("MyACL is --> ", acl)

     return self.ACL.create_acl(acl['id'],acl)

    # Test this
    def get_object_acl(self, acl_id):
      ref= acl.get_acl(acl_id)
      return ref


class Deserializer(wsgi.JSONRequestDeserializer):
    """Handles deserialization of specific controller method requests."""

    def _deserialize(self, request):
        result = {}
        return result

    def create(self, request):
        return self._deserialize(request)

    def update(self, request):
        return self._deserialize(request)


class Serializer(wsgi.JSONResponseSerializer):
    """Handles serialization of specific controller method responses."""

    def __init__(self):
        self.notifier = None

    def meta(self, response, result):
       return response

    def show(self, response, result):
        return response

    def update(self, response, result):
       return response

    def create(self, response, result):
       return response


def create_resource():
    """Resource factory method"""
    deserializer = Deserializer()
    serializer = Serializer()
    return wsgi.Resource(Controller(), deserializer, serializer)
