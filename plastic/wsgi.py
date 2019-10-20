# -*- coding: utf-8 -*-

from werkzeug.middleware.proxy_fix import ProxyFix

from .app import create_app

__all__ = ['app']

app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app)
