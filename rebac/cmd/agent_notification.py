# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from rebac import listener
from rebac.openstack.common import service as os_service
from rebac import service


def main():
    service.prepare_service()
    launcher = os_service.ProcessLauncher()
    launcher.launch_service(
        listener.ListenerService(),
        workers=service.get_workers('listener'))
    launcher.wait()

if __name__ == "__main__":
    main()
