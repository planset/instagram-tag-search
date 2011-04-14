import os

def numCpus():
    if not hasattr(os, 'sysconf'):
        raise RuntimeError('No sysconf detected.')
    return os.sysconf('SC_NPROCESSORS_ONLN')

bind = 'unix:/var/run/gunicorn/its.sock'
workers = numCpus() * 2 + 1
worker_class = 'egg:meinheld#gunicorn_worker'
pidfile = '/var/run/gunicorn/its.pid'

