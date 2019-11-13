# -*- coding: utf-8 -*-
# !/usr/bin/env python

from __future__ import absolute_import

from flask_migrate import MigrateCommand
from flask_script import Manager

from plastic.libs.db.store import db
from .wsgi import app

manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    """Run With shell context."""
    return {'app': app, 'db': db}


@manager.command
def runserver(host=None, port=None, workers=None):
    """Run the app with Gunicorn."""
    host = host or app.config.get('HTTP_HOST') or '0.0.0.0'
    port = port or app.config.get('HTTP_PORT') or 5000
    workers = workers or app.config.get('HTTP_WORKERS') or 1
    use_evalex = app.config.get('USE_EVALEX', app.debug)
    app.run(host, int(port), use_evalex=use_evalex)

    if app.debug:
        app.run(host, int(port), use_evalex=use_evalex)
    else:
        from gunicorn.app.wsgiapp import WSGIApplication
        gunicorn = WSGIApplication()
        gunicorn.load_wsgiapp = lambda: app
        gunicorn.cfg.set('bind', '%s:%s' % (host, port))
        gunicorn.cfg.set('workers', workers)
        gunicorn.cfg.set('pidfile', None)
        gunicorn.cfg.set('worker_class', 'gunicorn.workers.ggevent.GeventWorker')
        gunicorn.cfg.set('accesslog', '-')
        gunicorn.cfg.set('errorlog', '-')
        gunicorn.cfg.set('timeout', 300)
        gunicorn.chdir()
        gunicorn.run()


def main():
    manager.run()


if __name__ == '__main__':
    manager.run()
