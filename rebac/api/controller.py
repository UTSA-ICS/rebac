
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
from rebac.db import sql
from rebac.api import policy
from rebac import i18n
from rebac.i18n import _
_LI = i18n._LI
_LE = i18n._LE


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
      self.Relation = sql.RelationshipOperation()

    def user_authorized(self, req):
      return False

    def create_relationship(self, req, body):
      relationship ={}
      relationship['id'] = uuid.uuid4().hex
      relationship['sourcefile']= str(body['relationship']['sourcefile'])
      relationship['targetfilelist']= str(body['relationship']['targetfilelist'])
      return self.Relation.create_relationship(relationship['id'],relationship)

    def get_relationship(self, req, body):
      try:
        return self.Relation.get_relationship_by_sourcefilename(str(body['sourcefilename']))
      except exception.NotFound as e:
        msg = _("The Specified Relationship [%s] is Not Found") % e.message
        LOG.info(msg)
        return null;

    def delete_relationship(self, req, body):
      self.Relation.delete_relationship(str(body['sourcefilename']))
      return True

    def create_object_acl(self, req, body):
      acl = {}
      acl['id'] = uuid.uuid4().hex
      acl['sourcefile']= str(body['acl']['sourcefilename'])
      acl['userlist']= str(body['acl']['userlist'])

      print("MyACL is --> ", str(body['acl']))
      return self.ACL.create_acl(acl['id'],acl)

    # Test this
    def get_object_acl(self, req, body):
      try: 
        ref= self.ACL.get_acl_by_name(str(body['sourcefilename']))
        return ref
      except exception.NotFound as e:
        msg = _("The Specified ACL [%s] is Not Found") % e.message
	LOG.info(msg)
	return False;
    
    def delete_object_acl(self, req, body):
      return self.ACL.delete_acl(str(body['sourcefilename'])) 

    def _allowAccessThroughRelationship(self, userName, fileName):
      try:
	ref = self.Relation.get_relationship_by_sourcefilename(fileName)
      except exception.NotFound as e:
        msg = _("The Specified Relationship [%s] is Not Found") % e.message
        LOG.info(msg)
        return False;

      FileList= ref['targetfilelist'].split(',')
      print(FileList)
      for linkedFile in FileList:
	      print('Linked File:'+ linkedFile)
      	      if linkedFile in FileAlreadyVisited:
                 continue
      	      else:
                 FileAlreadyVisited.append(linkedFile)
                 if allowAccessThroughACL(userName, linkedFile):
                    return True
                 else:
                    return allowAccessThroughRelationship(userName, linkedFile)
      return False


    def _allowAccessThroughACL(self, userName, fileName):
         try:
           ref = self.ACL.get_acl_by_name(fileName) 
         except exception.NotFound as e:
           msg = _("The Specified ACL [%s] is Not Found") % e.message
           LOG.info(msg)
           return False;

         if userName in ref['userlist']:
            return True
         else:
            return False
      
    def authorize_access(self, req, body): 
       print("Checking ACL Status")
       ACLStatus = self._allowAccessThroughACL(str(body['username']), str(body['sourcefilename']))

       if ACLStatus :
          print(str(body['username']),'is allowed to Access', str(body['sourcefilename']), 'through ACL')
          return True 
       else:
          print(str(body['username']), 'not allowed to access',str(body['sourcefilename']), 'through ACL')
          ReBACStatus = self._allowAccessThroughRelationship(str(body['username']), str(body['sourcefilename']))

       if ReBACStatus:
          print(str(body['username']),'is allowed to access', str(body['sourcefilename']),'through relationship')
          return True
       else:
          print(str(body['username']),'is not allowed to access',str(body['sourcefilename']),'through relationship')
          return False

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
