# -*- coding: utf-8 -*-

## do not deploy this file and any other 00_local folder or file

if not request.env.web2py_runtime_gae:
    from gluon.custom_import import track_changes
    track_changes(True)

configuration = AppConfig(reload=False)

if not configuration.get('app.production'):
    response.generic_patterns.append('*')

mail.settings.server = 'logging'

auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = False