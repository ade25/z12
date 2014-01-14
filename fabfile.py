from fabric.api import cd
from fabric.api import env
from fabric.api import local
from fabric.api import run
from fabric.api import task

from ade25.fabfiles import project
from ade25.fabfiles.server import controls
from ade25.fabfiles import hotfix as hf

env.use_ssh_config = True
env.forward_agent = True
env.port = '22222'
env.user = 'root'
env.code_user = 'root'
env.prod_user = 'www'
env.webserver = '/opt/webserver/buildout.webserver'
env.code_root = '/opt/webserver/buildout.webserver'
env.host_root = '/opt/sites'

env.hosts = ['6zu4']
env.hosted_sites = [
    'xpose',
    'folia',
    'tophotel',
    'adk',
    'rheacting',
    're',
    'newport',
    'ro',
    'oh',
    's14',
    'wigo',
]

env.hosted_sites_locations = [
    '/opt/sites/xpose/buildout.xpose',
    '/opt/sites/folia/buildout.folia',
    '/opt/sites/tophotel/buildout.tophotel',
    '/opt/sites/adk/buildout.adk',
    '/opt/sites/rheacting/buildout.rheacting',
    '/opt/sites/re/buildout.re',
    '/opt/sites/newport/buildout.newport',
    '/opt/sites/ro/buildout.ro',
    '/opt/sites/oh/buildout.oh',
    '/opt/sites/oh/buildout.s14',
    '/opt/sites/oh/buildout.wigo',
]


@task
def push():
    """ Push committed local changes to git """
    local('git push')


@task
def restart():
    """ Restart all """
    with cd(env.webserver):
        run('nice bin/supervisorctl restart all')


@task
def restart_nginx():
    """ Restart Nginx """
    controls.restart_nginx()


@task
def restart_varnish():
    """ Restart Varnish """
    controls.restart_varnish()


@task
def restart_haproxy():
    """ Restart HAProxy """
    controls.restart_haproxy()


@task
def ctl(*cmd):
    """Runs an arbitrary supervisorctl command."""
    with cd(env.webserver):
        run('nice bin/supervisorctl ' + ' '.join(cmd))


@task
def deploy():
    """ Deploy current master to production server """
    push()
    controls.update()
    controls.build()


@task
def deploy_site():
    """ Deploy a new site to production """
    push()
    controls.update()
    controls.build()
    controls.reload_supervisor()


@task
def hotfix(addon=None):
    """ Apply hotfix to all hosted sites """
    hf.prepare_sites()
    hf.process_hotfix()
