import os

from fabric.api import *
from backupator.conf import settings

DEPENDENCIES_COMMANDS = {
	"ubuntu/linux" : "sudo apt-get install python-dev python-fuse python-pyxattr python-pylibacl"
}


@task
def install(operating_system="ubuntu/linux"):
	build_dir = os.path.join(settings.PROJECT_PATH, "build", "bup")
	local("mkdir -p %s" % (build_dir,))
	with lcd(build_dir):
		local("rm -rf src")
		local("git clone git://github.com/apenwarr/bup src")
		local(DEPENDENCIES_COMMANDS.get(operating_system))
		
		dirs = [
			"usr/share/man",
			"usr/share/doc/bup",
			"usr/bin",
			"usr/lib/bup",
		]

		for d in dirs:
			local("mkdir -p %s" % (d,))

		with lcd("src"):
	 		local("DESTDIR=%s make" % build_dir, )
	 		local("DESTDIR=%s make install" % build_dir, )

