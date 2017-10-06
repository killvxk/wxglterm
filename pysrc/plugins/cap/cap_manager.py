import logging
import sys

from . import unknown_cap

def get_cap_handler(name):
    logging.getLogger('cap_manager').debug("cap:{}".format(name))

    # Fast path: see if the module has already been imported.
    try:
        return sys.modules['cap.' + name]
    except KeyError:
        pass

    try:
        #fp, pathname, description = imp.find_module(name, [os.path.dirname(__file__)])
        #return imp.load_module(name, fp, pathname, description)
        __import__('cap.' + name)

        return sys.modules['cap.' + name]
    except ImportError:
        return unknown_cap
