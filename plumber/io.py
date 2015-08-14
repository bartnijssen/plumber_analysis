"""
io module for plumber data
"""
import configparser
import logging
import re
import xray
from . import utils


def ingest(infile, read_vars, tshift=None):
    """
    read input and output files from the plumber experiment

    Parameters
    ----------
    Required:
        infile : string
            input file name (netcdf format)
        read_vars : list or string ('all')
            list of variables to read from infile. If read_vars == 'all' then
            all variables are retained.
    Default:
        tshift :
            time shift in minutes (default=None)

    Returns
    -------
    ds : pandas dataframe
        data frame with those elements in read_vars that are present in infile

    The returned dataframe is not guaranteed to have all the variables that are
    specified in read_vars. It will only include those that are available. It
    is up to the user to check for completeness.
    """

    # make a copy of read_vars since we don't want to change the list in the
    # calling scope
    if read_vars != 'all':
        try:
            read_vars = read_vars.copy()
        except AttributeError as err:
            logging.critical('%s: read_vars should be a list or \'all\'', err)
            raise

    # read infile using xray
    ds = xray.open_dataset(infile, decode_times=False)

    # find the time dimension
    time_dim = [x for x in ds.dims if re.search('time', x, re.I)][0]

    # rename the time dimension to 'time' to make life easier
    if time_dim != 'time':
        ds.rename({time_dim: 'time'}, inplace=True)

    # only keep the time dimension, drop the others
    dims = [x for x in ds.dims if x != 'time']

    # select the [0] element for all for dimensions
    dd = dict(zip(dims, [0]*len(dims)))
    ds = ds.isel(**dd)

    # drop all non-time dimensions
    ds = ds.drop(dims)

    # reconstruct Rnet if it is not provided
    if 'Rnet' in read_vars or read_vars == 'all':
        if 'Rnet' not in ds.variables:
            try:
                ds['Rnet'] = ds['SWnet'] + ds['LWnet']
            except KeyError:
                pass

    # drop all variables that are not in read_vars (but keep time)
    if read_vars != 'all':
        read_vars.append('time')
        ds = ds.drop(list(set(ds.variables) - set(read_vars)))

    # align the time according to tshift
    # The easiest way to do this would be to use
    # ds = ds.tshift(tshift, freq='T')
    # However, the tshift() method is currently very slow, so we do the
    # shift on the raw time axis and then decode after
    if tshift:
        ds.time += tshift*60
    ds = xray.decode_cf(ds, decode_times=True)

    # convert to dataframe
    df = ds.to_dataframe()

    # some of the time stamps in PLUMBER are messed up
    # regularize
    df = df.asfreq('30Min', method='nearest')

    return df


def parseConfig(configfile=None):
    """Parse a configuration file and return the configuration as a
       dictionary"""
    if configfile is None:
        return {}
    cfgparser = \
        configparser.ConfigParser(allow_no_value=True,
                                  interpolation=configparser.
                                  ExtendedInterpolation())

    cfgparser.optionxform = str  # preserve case of configuration keys
    logging.debug('Reading %s', configfile)
    cfgparser.read(configfile)
    # convert the cfgparser to an easier to handle dictionary
    cfg = {}
    for section in cfgparser.sections():
        cfg[section.lower()] = {}
        for key in cfgparser[section]:
            cfg[section.lower()][key.lower()] = cfgparser[section][key]

    # convert dictionary values. First convert any comma-separated entries
    # to lists, then convert entries to boolean, ints, and floats
    # strings with a trailing zero are also converted to a list
    for section, options in cfg.items():
        for key, val in options.items():
            if re.search(',', val):
                cfg[section][key] = [x.strip() for x in val.split(',')
                                     if x.strip()]
            if isinstance(cfg[section][key], list):
                cfg[section][key] = [utils.cast(x) for x in cfg[section][key]]
            else:
                cfg[section][key] = utils.cast(cfg[section][key])
    logging.debug('Parsed configuration file %s', configfile)
    return cfg
