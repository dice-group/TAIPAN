try:
   import cPickle as pickle
except:
   import pickle

import os

from taipan.pathes import DEFAULT_CACHE_DIR

CACHE_DIR = os.environ.get("TAIPAN_CACHE_DIR", DEFAULT_CACHE_DIR)

def enable_cache(object_type):
    def _enable_cache(func):
        def wrapper(self, *args):
            filename = "%s_%s.cache" % (args[0]._id, object_type)
            filepath = os.path.join(CACHE_DIR, filename)
            if(os.path.exists(filepath)):
                return pickle.load(open(filepath, 'rb'))
            else:
                result = func(self, *args)
                pickle.dump(result, open(filepath, "wb" ))
                return result
        return wrapper
    return _enable_cache
