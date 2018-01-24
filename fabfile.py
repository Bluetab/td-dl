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
    run('rm -rf /home/ec2-user/data-lineage/venv')
    run('virtualenv -p python3 /home/ec2-user/data-lineage/venv')

    # install the package in the application's virtualenv with pip
    run('/home/ec2-user/data-lineage/venv/bin/pip install /tmp/%s' % filename)

    # remove the uploaded package
    run('rm -r /tmp/%s' % filename)

    # remove the uploaded package
    run('nohup sh -c "/home/ec2-user/data-lineage/venv/bin/gunicorn --bind 0.0.0.0:5000 api:app" > /home/ec2-user/data-lineage/data-lineage.log 2>&1&')

    # touch the .wsgi file to trigger a reload in mod_wsgi
    #run('touch /home/ec2-user/data-lineage.wsgi')
