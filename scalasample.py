import sys
import pprint
import ansible.runner
from ansible import inventory

installDocker = ansible.runner.Runner(
	remote_user='root',
	remote_pass=None,
	module_name='apt',
	module_args='pkg=docker.io state=latest update_cache=true',
	inventory=inventory.Inventory(sys.argv[1])
)

print("Installing Docker.io")
getFacts = installDocker.run()
pprint.pprint(getFacts)
print(getFacts['contacted']['192.168.1.28']['stdout'])
