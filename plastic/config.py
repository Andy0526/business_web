# -*- coding: utf-8 -*-

DEBUG = False
HTTP_PORT = 80
SECRET_KEY = "business_web-secret"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SESSION_COOKIE_HTTPONLY = False

if DEBUG:
    SENTRY_RELEASE = u"测试环境"
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "postgresql://business:1vbrcu2@localhost:5432/business"
else:
    SENTRY_RELEASE = u"线上环境"
    TESTING = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = "postgresql://business:1vbrcu2@localhost:5432/business"
