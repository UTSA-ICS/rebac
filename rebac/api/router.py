# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 OpenStack Foundation.
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

from rebac.api import controller
from rebac.common import wsgi


class API(wsgi.Router):

    """WSGI router for REBAC API requests."""

    def __init__(self, mapper):

        rebac_resource = controller.create_resource()
        mapper.connect('/rebac/create_object_acl',
                       controller=rebac_resource,
                       action='create_object_acl',
                       conditions={'method': ['POST']})
        mapper.connect('/rebac/get_object_acl',
                       controller=rebac_resource,
                       action='get_object_acl',
                       conditions={'method': ['GET']})
        mapper.connect('/rebac/user_authorized',
                       controller=rebac_resource,
                       action='user_authorized',
                       conditions={'method': ['GET']})

        super(API, self).__init__(mapper)
