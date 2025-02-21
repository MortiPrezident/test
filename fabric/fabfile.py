import os
from fabric import Connection, task


@task
def deploy(ctx):
   key_path = os.path.expanduser("~/.ssh/id_ed25519")
   with Connection(
       os.environ["HOST"],
       user=os.environ["USER_NAME"],
       connect_kwargs={"key_filename": os.environ["PRIVATE_KEY"]}
   ) as c:
       with c.cd("/home/test"):
           c.run("docker compose down")
           c.run("git pull origin main --rebase")
           c.run("docker compose up --build -d")