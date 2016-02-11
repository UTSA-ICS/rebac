# Copyright 2012 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslo_config import cfg
from rebac.common import utils
from rebac.common import exception
from rebac.i18n import _
from rebac.common import sql

CONF = cfg.CONF

class Relationship(sql.ModelBase, sql.DictBase):
  __tablename__ = 'relationship'
  attributes = ['id', 'sourcefile', 'targetfilelist']
  id = sql.Column(sql.String(64), primary_key=True)
  sourcefile = sql.Column(sql.String(256), nullable=False)
  targetfilelist = sql.Column(sql.String(1024),nullable=False)

class ACL(sql.ModelBase, sql.DictBase):
  __tablename__ = 'acl'
  attributes = ['id', 'sourcefile', 'userlist']
  id = sql.Column(sql.String(64), primary_key=True)
  sourcefile = sql.Column(sql.String(256), nullable=False)
  userlist = sql.Column(sql.String(1024),nullable=False)

class RelationshipOperation():

  def __init__(self):
    print("RelationshipOperation")

  @property
  def is_sql(self):
    return True

  @sql.handle_conflicts(conflict_type='relationship')
  def create_relationship(self, id, relationship):
    session = sql.get_session()
    with session.begin():
      relationship_ref = Relationship.from_dict(relationship)
      session.add(relationship_ref)
      return  relationship_ref.to_dict()

  def get_relationship_by_sourcefilename(self,sourcefilename):
    session = sql.get_session()
    query = session.query(Relationship)
    query = query.filter_by(sourcefile=sourcefilename)
    try:
      relationship_ref = query.one()
    except sql.NotFound:
      raise exception.UserNotFound(id=id)
    return relationship_ref.to_dict()

  def delete_reltionship(self,sourcefilename):
    session = sql.get_session()
    with session.begin():
      ref = self._get_relationship_by_sourcefilename(session, sourcefilename)
      q = session.query(Relationship)
      q = q.filter_by(id=id)
      q.delete(False)
      session.delete(ref)

class ACLOperation():
  def __init__(self):
    print("ACLOperation")

  def is_sql(self):
    return True

  def create_acl(self,id, acl):
    session = sql.get_session()
    with session.begin():
      acl_ref = ACL.from_dict(acl)
      session.add(acl_ref)
      return  acl_ref.to_dict()

  def _get_acl(self, session, acl_id):
    ref = session.query(ACL).get(acl_id)
    if not ref:
      raise exception.UserNotFound(acl_id=acl_id)
    return ref

  def get_acl(self, acl_id):
    session = sql.get_session()
    return identity.filter_user(self._get_acl(session, acl_id).to_dict())

  def get_acl_by_name(self,sourcefilename):
    session = sql.get_session()
    query = session.query(ACL)
    query = query.filter_by(sourcefile=sourcefilename)
    try:
      acl_ref = query.one()
    except sql.NotFound:
      raise exception.UserNotFound()
    return acl_ref.to_dict()

  def delete_acl(self,sourcefilename):
    session = sql.get_session()
    with session.begin():
      ref = self._get_acl_by_sourcefilename(session, sourcefilename)
      q = session.query(ACL)
      q = q.filter_by(id=id)
      q.delete(False)
