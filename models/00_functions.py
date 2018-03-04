# -*- coding: utf-8 -*-

def STATIC(*args, **kwargs):
    kwargs['language'] = configuration.get('app.locale', T.get_possible_languages_info()['default'][0])
    return URL('static', *args, **kwargs)