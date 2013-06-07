import logging
import os
import pytz
from randblock.config import LazyConfigValue


class Config(object):
    """Base config to work from"""
    ENVIRONMENT = 'live'
    BASIC_LOG_LEVEL = logging.WARNING
    LOGGING_LEVEL = logging.WARNING
    EMAIL_LOGGING = False
    
    DEBUG = False
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    
    SECRET_KEY = '63fe3db58d1e3aa76432b6badbcafaea'
    SESSION_COOKIE_NAME = "c_ses"
    
    BASE_APP_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    TMP_DIR = os.path.join(ROOT_DIR, "tmp")
    
    STATIC_DIR = os.path.join(BASE_APP_DIR, "static")


class DevelopmentConfig(Config):
    """Development config"""
    
    ENVIRONMENT = 'development'
    BASIC_LOG_LEVEL = logging.DEBUG
    LOGGING_LEVEL = logging.DEBUG
    
    DEBUG = True
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

