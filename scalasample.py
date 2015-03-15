import sys
import os
import pprint
import ansible.runner
from ansible import inventory

"""
	Base Ansible runner builder.
"""
class AnsibleBase:
	"""
		Initializes the object.
	"""
	def __init__(self, hostInventory, hostIsFile=True):
		os.environ['ANSIBLE_HOST_KEY_CHECKING'] = 'False'
		if hostIsFile:
			self.hostInventory = inventory.Inventory(sys.argv[1])
	
	"""
		Makes a call to the ansible lib to create a runner.
	"""
	def buildRunner(self, moduleName, moduleArgs):
		return ansible.runner.Runner(
			remote_user='root',
			remote_pass=None,
			module_name=moduleName,
			module_args= moduleArgs,
			inventory=self.hostInventory
		)

	"""
		Builds and runs the ansible runners.
		@return list of resulting facts from the runners.
	"""
	def run(self):
		runners = self.generateRunners()
		return list(map(lambda x: self.doRun(*x), runners))

	@staticmethod
	def doRun(message, runner):
		print(message)
		runner.run()

"""
	Basic play based scala stack Installer.
"""
class ScalaPlayStack(AnsibleBase):
	
	"""
		Initializes the object
	"""
	def __init__(self, hostInventory, hostIsFile=True):
		AnsibleBase.__init__(self, hostInventory, hostIsFile)

	"""
		Generates a Docker install runner.
	"""
	def generateDockerInstallRunner(self):
		return ("Installing Docker.io", self.buildRunner('apt', 'pkg=docker.io state=latest update_cache=true'))
	
	"""
		Generates the runners to run.
		@return list of ansible runners.
	"""
	def generateRunners(self):
		runners = []
		
		runners.append(self.generateDockerInstallRunner())

		return runners


if len(sys.argv) == 2:
	playStack = ScalaPlayStack(sys.argv[1])
	pprint.pprint(playStack.run())
else:
	print("Usage: `python scalasample.py <hostfile>`")
