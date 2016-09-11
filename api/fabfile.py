from fabric.api import *

# the server where the commands are executed
bilal_hosts = ['admin@158.69.92.163', 'ubuntu@52.91.150.68']
marine_hosts = ['admin@158.69.77.113', 'ubuntu@54.175.88.51']

#file/folder name
name = 'airbnb_clone'
#remote code directory
remote_dir = '/var'

def test():
    tests = local('AIRBNB_ENV=test python -m unittest discover tests --pattern=*.py')
    if tests.failed:
        print "Tests failed. Aborting!"
        exit(1)

def pack():
    # create a tarball from local source folder
    local('tar czf /tmp/%s.tar.gz .' % (name))

def deploy():
    test()
    # create a tarball from local source
    pack()
    # upload the source tarball to the temporary folder on the server
    put('/tmp/%s.tar.gz' % name, '/tmp/%s.tar.gz' % name)
    with cd('/tmp'):
        #if the folder with the name of "name" already exists, delete it first
        run('rm -rf %s' % name)
        #create  directory in temp
        run('sudo mkdir -p %s/api' % name)
        # extract tar.gz
        run('sudo tar -xzf /tmp/%s.tar.gz -C /tmp/%s/api' % (name, name))
        run('sudo mkdir -p /var/%s' % name)
    with cd(remote_dir):
        # delete previous website folder and move the new folder in its place
        run('sudo rm -rf %s' % name)
        run('sudo mv /tmp/%s ./' % name)
        # remove temporary files
        run('rm -rf /tmp/%s /tmp/%s.tar.gz' % (name, name))
    local('rm -f /tmp/%s.tar.gz' % name)

'''deploy api files to servers of Bilal Khan'''
@hosts(bilal_hosts)  
def deploy_bilal():
    global env
    # custom directory for the ssh key
    env.key_filename = '~/.ssh_holberton/id_rsa_holberton'
    deploy()

'''deploy api files to servers of Marine Dejean'''
@hosts(marine_hosts)
def deploy_marine():
    deploy()