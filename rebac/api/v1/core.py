
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
/PDP endpoint for Sios v1 API
"""

import copy
import eventlet
from oslo_config import cfg
from webob.exc import (HTTPError,
                       HTTPNotFound,
                       HTTPConflict,
                       HTTPBadRequest,
                       HTTPForbidden,
                       HTTPRequestEntityTooLarge,
                       HTTPInternalServerError,
                       HTTPServiceUnavailable)
from webob import Response
from rebac.api import policy
import rebac.api.v1
from rebac.common import exception
from rebac.common import utils
from rebac.common import wsgi
from oslo_utils import strutils
import oslo_log.log as logging
from rebac.i18n import _
# Import db here
from rebac.db import sql

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class ReBAC(object):
    """
    WSGI controller for Policy Decision Point in Sios v1 API

    The PDP resource API is a RESTful web service for Policy Decisions. The API
    is as follows::

        POST /check -- check the Policy Decision
        POST /enforce -- check the Policy Decision to be enforced
    """

    # User CRUD

    def create_relationship(relationship):
     relationship['id'] =uuid.uuid4().hex
     return sql.create_relationship(relationship[id],relationship)

    def get_relationship(sourceFilename):
      ref = sql.get_relationship(sourcefilename)
      return ref

    # Test this
    def create_object_acl(acl):
     acl['id'] = uuid.uuid4().hex
     return self.sql.create_acl(acl[id],acl)

    # Test this
    def get_object_acl(acl_id):
      ref= self.sql.get_acl(acl_id)
      return ref

    #def update_relationship():
    #def delete_relationship():
    #def update_object_acl():
    #def delete_object_acl():
