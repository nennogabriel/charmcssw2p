# -*- coding: utf-8 -*-

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

## Imports
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

config = AppConfig(reload=False)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(config.get('db.uri'),
             pool_size=config.get('db.pool_size'),
             migrate_enabled=config.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    # session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    from gluon.contrib.memdb import MEMDB
    from google.appengine.api.memcache import Client
    session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------


response.generic_patterns = []

response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=config.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
# auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = config.get('smtp.server')
mail.settings.sender = config.get('smtp.sender')
mail.settings.login = config.get('smtp.login')
mail.settings.tls = config.get('smtp.tls') or False
mail.settings.ssl = config.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# -------------------------------------------------------------------------
if request.extension == 'html' and not request.ajax:
    response.meta.application = config.get('app.name')
    response.meta.generator = config.get('app.generator')
    response.meta.description = T(config.get('app.description'))
    response.meta.author = config.get('app.author')
    response.meta.theme_color = config.get('app.theme_color')
    response.meta.apple_mobile_web_app_status_bar_style = config.get('app.apple_mobile_web_app_status_bar_style')
    response.title = config.get('app.name')
    response.subtitle = config.get('app.subtitle')

    # -------------------------------------------------------------------------
    # your http://google.com/analytics id
    # -------------------------------------------------------------------------
    response.google_analytics_id = config.get('google.analytics_id')


# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if config.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=config.get('heartbeat'))


# -------------------------------------------------------------------------
# Load Plugins
# -------------------------------------------------------------------------

from plugin_materialize import *
response.formstyle = formstyle_materialize
auth.settings.formstyle = formstyle_materialize
