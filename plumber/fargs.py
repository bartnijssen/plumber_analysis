"""
module for determining arguments required by a function
Expanded taken from
http://stackoverflow.com/questions/196960/
can-you-list-the-keyword-arguments-a-python-function-receives
"""
import inspect
from . import utils


def callFuncBasedOnDict(func, argdict, **kwargs):
    """ Call func by selecting appropriate arguments from a argdict as well as
        kwargs"""
    if argdict is None:
        argdict = {}
    seldict = selectArgsFromDict(func, argdict)
    if kwargs is not None:
        seldict.update(kwargs)
    return func(**seldict)


def getArgs(func):
    """get all arguments for a function"""
    # exclude the defaults at the end (hence the [:-1])
    args = list(utils.flatten(inspect.getargspec(func)[:-1]))
    return set(args).difference(set([None]))


def getRequiredArgs(func):
    "get required arguments for a function"
    args, varargs, varkw, defaults = inspect.getargspec(func)
    if defaults:
        args = args[:-len(defaults)]
    return args   # *args and **kwargs are not required, so ignore them.


def invalidArgs(func, argdict):
    """check for invalid args"""
    args, varargs, varkw, defaults = inspect.getargspec(func)
    if varkw:
        return set()  # All accepted
    return set(argdict) - set(args)


def isCallableWithArgs(func, argdict):
    """full test to determine whether a function is callable given arguments"""
    return not missingArgs(func, argdict) and not invalidArgs(func, argdict)


def missingArgs(func, argdict):
    """function to tell what you are missing from argdict"""
    return set(getRequiredArgs(func)).difference(argdict)


def selectArgsFromDict(func, argdict):
    """return subset of argdict that has acceptable arguments for func"""
    return dict([(i, argdict[i]) for i in getArgs(func) if i in argdict])
