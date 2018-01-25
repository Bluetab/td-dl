from fabric.api import *

# the user to use for the remote commands
env.user = 'ec2-user'
# the servers where the commands are executed
env.hosts = ['52.214.3.82']

def pack():
    # build the package
    local('python setup.py sdist --formats=gztar', capture=False)

def deploy():
    # figure out the package name and version
    dist = local('python setup.py --fullname', capture=True).strip()
    filename = '%s.tar.gz' % dist

    # upload the package to the temporary folder on the server
    put('dist/%s' % filename, '/tmp/%s' % filename)

    # upload env
    run('sudo rm -rf /home/ec2-user/data-lineage/venv')
    run('virtualenv -p python3 /home/ec2-user/data-lineage/venv')

    # install the package in the application's virtualenv with pip
    run('/home/ec2-user/data-lineage/venv/bin/pip install /tmp/%s' % filename)

    # remove the uploaded package
    run('rm -r /tmp/%s' % filename)

    # restart lineage service
    run('touch /home/ec2-user/data-lineage/wsgi.py && \
         rm /home/ec2-user/data-lineage/wsgi.py')

    put("wsgi.py", "/home/ec2-user/data-lineage/wsgi.py")

    run("sudo initctl stop lineage")
    run("sudo initctl start lineage")
