"""todo: move here all functions related to languages
in other utils modules
"""
from askbot.conf import settings as askbot_settings
from django.conf import settings as django_settings
from django.utils.encoding import force_str
from django.utils import translation

def get_language():
    if getattr(django_settings, 'ASKBOT_MULTILINGUAL', False):
        return translation.get_language()
    elif HAS_ASKBOT_LOCALE_MIDDLEWARE:
        return askbot_settings.ASKBOT_LANGUAGE
    else:
        return django_settings.LANGUAGE_CODE

HAS_ASKBOT_LOCALE_MIDDLEWARE = 'askbot.middleware.locale.LocaleMiddleware' in \
                                   django_settings.MIDDLEWARE_CLASSES

LANGUAGES_DICT = dict(django_settings.LANGUAGES)

def get_language_codes():
    """returns list of activated language codes"""
    return LANGUAGES_DICT.keys()

def get_language_name(lang=None):
    lang = lang or get_language()
    return force_str(LANGUAGES_DICT[lang])
