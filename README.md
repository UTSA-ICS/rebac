rebac
====

REBAC PDP service for Openstack

This service will act as a Policy Decision Point (PDP) for any OpenStack service.<br>
A OpenStack service's Policy Enforcement engine will make a REST call to REBAC PDP service for a Policy Decision.<br>
The REBAC PDP service will always respond with a 'True' of 'False' as a result of the Policy Query.<br>
In addition to the standard OpenStack HTTP headers, the follwing two HTTP headers are required by REBAC PDP api:<br>
1. 'X-Action'<br>
2. 'X-Target'

First you will need to download the rebac project:<br>
a.) cd /opt/stack<br>
b.) git clone https://github.com/UTSA-ICS/rebac.git<br>
c.) sudo mkdir /etc/rebac/<br>

To be able to use this service do the following:<br>
1.) Copy rebac/etc to /etc/rebac<br>
sudo cp /opt/stack/rebac/etc/* /etc/rebac/.<br>
2.) Create a directory called /var/cache/rebac and give it 777 permission<br>
sudo mkdir /var/cache/rebac<br>
sudo chmod 777 /var/cache/rebac<br>
3.) Create a user [rebac] with password [admin] in the service tenant with 'admin' role<br>
keystone user-create --name rebac --pass admin --enabled true<br>
keystone user-role-add --user rebac --role admin --tenant service<br>
4.) Create a service called 'rebac' in Keystone<br>
keystone service-create --type rebac --name rebac --description "Relationship based access control"<br>
5.) To start the REBAC service run the following commands:<br>
cd /opt/stack; sudo pip install -e rebac<br>
cd /opt/stack/rebac; /opt/stack/rebac/bin/rebac-api --config-file=/etc/rebac/rebac-api.conf || touch "/opt/stack/status/stack/rebac-api.failure"<br>
6.) Restart nova api and glance api services (from screen)<br>

To Test Usage:
==============
- Run nova commands (e.g. nova list)
- Run glance commands (e.g glance image-list)
