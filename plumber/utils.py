"""
Utility functions for plumber
"""
import numpy as np


def budyko(x):
    """Budyko curve function based on Koster et al. 2006:
       http://dx.doi.org/10.1029/2006jd007182
       Suggested usage: budyko(np.linspace(0,10,100))"""
    b = x * np.tanh(x**(-1)) * (1 - np.cosh(x) + np.sinh(x))
    b = np.sqrt(b)
    return b


def cast(x):
    for f in (int, float, toBool, toNone):
        try:
            return f(x)
        except (TypeError, ValueError):
            pass
    return x


def flatten(*args):
    """flatten a list of lists"""
    for x in args:
        if not isinstance(x, str) and hasattr(x, '__iter__'):
            for y in flatten(*x):
                yield y
        else:
            yield x


def lv(T, units='K'):
    """Calculate the latent heat of vaporization as a function of temperature.
       Results are in J/kg
       https://en.wikipedia.org/wiki/Latent_heat
       #Latent_heat_for_condensation_of_water"""
    if units == 'K':
        T -= 273.16
    elif units == 'C':
        pass
    else:
        raise(ValueError)
    L = 2500.8 - 2.36*T + 0.0016*T**2 - 0.00006*T**3
    L *= 1000.
    return L


def toBool(x):
    """Convert a string to a boolean value. Just throw exception if it does not
       work."""
    if x.lower() == 'true':
        return True
    elif x.lower() == 'false':
        return False
    else:
        raise ValueError


def toNone(x):
    """Convert a string that spells out 'None' (case insensitive) to the
       python None value"""
    if x.lower() == 'none':
        return None
    else:
        raise ValueError
