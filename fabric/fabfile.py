import os
from fabric import Connection, task


@task
def deploy(ctx):
   key_path = os.path.expanduser("~/.ssh/id_ed25519")
   with Connection(
       "147.45.104.71",
       user="root",
       connect_kwargs={"key_filename": "{key_path}".format(key_path=key_path)}
   ) as c:
       with c.cd("/home/"):
           c.run("ls -la")
           c.run("uname -a")