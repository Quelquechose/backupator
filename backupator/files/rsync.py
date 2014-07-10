
from fabric.api import *
from backupator.conf import settings
from backupator.api import lrun, get_backup_dir, current_hostdef, is_force_local


from fabric.contrib import project


def get_settings():
    hostdef = current_hostdef()
    rsync = hostdef.get("rsync")
    dirs  = rsync.get("dirs")
    options  = rsync.get("options", "")
    delete = rsync.get("delete", False)
    exclude = rsync.get("host", "")
    return (dirs, options, delete, exclude)


@task
@roles("rsync")
def backup():
	dirs, options, delete, exclude = get_settings()

	for d in dirs:
		local_dir = d[0]
		remote_dir = d[1]

		project.rsync_project(
			local_dir=local_dir, remote_dir=remote_dir, 
			delete=delete, extra_opts=options)