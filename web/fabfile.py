from fabric.api import *

# the user to use for the remote commands
#env.user = 'admin'
# the server where the commands are executed
bilal_hosts = ['admin@158.69.92.163', 'ubuntu@52.91.150.68']
marine_hosts = ['admin@158.69.77.113', 'ubuntu@54.175.88.51']
#env.hosts = ['158.69.92.163']

#file/folder name
name = 'airbnb_web'
#remote code directory
remote_dir = '/data/apps'

def pack():
    # create a tarball from local source folder
    local('tar czf /tmp/%s.tar.gz index.html static/*' % (name))

def deploy():
    # create a tarball from local source
    pack()
    # upload the source tarball to the temporary folder on the server
    put('/tmp/%s.tar.gz' % name, '/tmp/%s.tar.gz' % name)
    with cd('/tmp'):
        #if the folder with the name of "name" already exists, delete it first
        run('rm -rf %s' % name)
        #create  directory in temp
        run('sudo mkdir -p %s' % name)
        # extract tar.gz
        run('sudo tar -xzf /tmp/%s.tar.gz -C /tmp/%s/' % (name, name))
        run('sudo mkdir -p /data/apps/%s' % name)
    with cd(remote_dir):
        # delete previous website folder and move the new folder in its place
        run('sudo rm -rf %s' % name)
        run('sudo mv /tmp/%s ./' % name)
        # remove temporary files
        run('rm -rf /tmp/%s /tmp/%s.tar.gz' % (name, name))
    local('rm -f /tmp/%s.tar.gz' % name)

@hosts(bilal_hosts)  
def deploy_bilal():
    global env
    # custom directory for the ssh key
    env.key_filename = '~/.ssh_holberton/id_rsa_holberton'
    deploy()

@hosts(marine_hosts)
def deploy_marine():
    deploy()
