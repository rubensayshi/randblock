from randblock.backend.UserDict import UserDict
from stringlike import StringLike
from werkzeug.utils import import_string


ENVIRON_VAR = 'ENVIRONMENT'
DEFAULT_ENVIRONMENT = 'development'


def dict_from_object(obj):
    """copy&paste from flask.Config class"""
    dict = {}
    
    if isinstance(obj, basestring):
        obj = import_string(obj)
    
    for key in dir(obj):
        if key.isupper():
            dict[key] = getattr(obj, key)
    
    return dict


def validate_env(env):
    assert env in ['development', 'test', 'staging', 'live']


class Environment(StringLike):
    def __init__(self, env = None):
        if env:
            validate_env(env)
        
        self._env = env
    
    @property
    def env(self):
        if self._env is None:
            import os
            self._env = os.environ.get(ENVIRON_VAR, DEFAULT_ENVIRONMENT)
        
        return self._env
    
    def __str__(self):
        return self.env


# init environment
environment = Environment()


class EnvironmentConfig(UserDict):
    """inherit from UserDict (without calling it's __init__) 
        so that we can provide our own (lazy loading) self.data - containing our config"""
    
    def __init__(self, environment = None, *args, **kwargs):
        self._environment = environment
        self._data = None
    
    def __getitem__(self, attr):
        v = super(EnvironmentConfig, self).__getitem__(attr)
        
        if isinstance(v, LazyConfigValue):
            self[attr] = v.value
            return self.__getitem__(attr)
        
        return v
    
    @property
    def environment(self):
        return str(self._environment or environment)
    
    @property
    def data(self):
        if self._data is None:
            self._data = {}
            self._data.update(dict_from_object('randblock.config.configs.' + self.environment.capitalize() + 'Config'))
            
            try:
                self._data.update(dict_from_object('randblock.config.config_local'))
            except ImportError:
                pass
        
        return self._data


# init config
config = EnvironmentConfig()


class Version(StringLike):
    def __init__(self, version_name):
        self.version_name = version_name
        self._version     = None
    
    @property
    def is_dev(self):
        return config['ENVIRONMENT'] == 'development'
    
    @property
    def version(self):
        from time import time
        
        if self._version is None:
            self._version = self.get_version()
        
        return self._version if self._version else str(int(time()))
    
    def get_version(self):
        import os
        
        if not self.is_dev:
            return self._get_version()
        else:
            if config['VERSION_ON_DEV'] and isinstance(config['VERSION_ON_DEV'], basestring):
                # version needs to be VERSION_STRING_LENGTH long for some of our sanity checks
                return str(config['VERSION_ON_DEV']).rjust(config['VERSION_STRING_LENGTH'], "_")
            elif config['VERSION_ON_DEV']:
                return self._get_version()
            else:
                return None
    
    def _get_version(self):
        import os
        version_file = os.path.join(config['ROOT_DIR'], "VERSION")
        
        if not os.path.exists(version_file):
            raise Exception("VERSION file not found")
        
        try:
            f = open(version_file, "r")
            data = f.read().split("\n")
            
            for line in data:
                line = str(line).split("=")
                if len(line) == 2:
                    if line[0] == self.version_name:
                        return line[1]
        except:
            raise Exception("Failed to parse VERSION file")
        
        raise Exception("Failed to find version [%s] in VERSION file" % self.version_name)
    
    def __str__(self):
        return self.version


# init versions
MAIN_VERSION   = Version("MAIN_VERSION")
STATIC_VERSION = Version("STATIC_VERSION")
APP_VERSION    = Version("APP_VERSION")

class LazyConfigValue(object):
    """LazyConfigString provides a way to do lazy string replacements.
        this allows us to overload the values that are used in the replacement in our env specific classes.
        
        we inherit StringLike which provides all the usual string operations and it's all done on str(self),
         so all we have to do is provide __str__
        
        for example: 
            class Config(object): 
                REDIS_SERVER=  'localhost'; 
                REDIS_URL = LazyConfigString('redis://%(REDIS_SERVER)s:9999/1')
            
            class DevConfig(Config):
                REDIS_SERVER = 'redis1.dev'
        
            print DevConfig().REDIS_URL # redis://redis1.dev:9999/1
        """
    
    def __init__(self, pattern, type = str):
        self._type    = type
        self._pattern = pattern
        self._value   = None
    
    @property
    def config(self):
        return config
    
    @property
    def pattern(self):
        return self._pattern
    
    @property
    def value(self):
        # generate the value if we haven't already
        if self._value is None:
            if self.pattern in self.config:
                self._value = self.config[self.pattern]
            else:
                self._value = self.pattern % self.config
            
            self._value = self._type(self._value)
        
        return self._value
    
    def __repr__(self):
        return "<LazyConfigValue %s: %s>" % (self.pattern, self.value)