
from oslo_config import cfg
from sios.common import utils
from sios.common import exception
from sios.i18n import _


class ACLOperation():
  def __init__(self):
    print("ACLOperation")
  def is_sql(self):
    return True
  def create_acl(self,id, acl):
    session = sql.get_session()
    with session.begin():
    acl_ref = ACL.from_dict(acl)
    session.add(user_ref)
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
