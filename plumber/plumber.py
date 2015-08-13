import configparser
import logging
import os
import pickle
import sys
from . import io

loglevel_default = 'info'


class PlumberAnalysis(object):
    """Overarching class for organizing analysis of the PLUMBER dataset.
       Acts as a container for all the info that is associated with a
       particular set of analysis."""

    def __init__(self, configfile=None):
        """Initialize PlumberAnalysis instance based on a configuration file"""
        self.cfg = {}
        self.configfile = configfile
        if self.configfile:
            self.cfg = io.parseconfig(self.configfile)
        self.data = {}
        # Since data is not pickled as part of the class instance, we maintain
        # a separate data_dict to help restore_data()
        self.data_dict = {}

    def __getstate__(self):
        """Define what will be pickled"""
        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()
        # Remove the unpicklable entries. In this case, the data entries
        # will be pickled separately, to avoid the python bug with writing
        # large files on OS X
        del state['data']
        return state

    def ingest(self, site, source, *args, **kwargs):
        """Ingest a timeseries for a given site and source. All variables other
           than site and source are simply handed to plumber.io.ingest"""
        if site not in self.data:
            self.data[site] = {}
            self.data_dict[site] = []
        self.data[site][source] = io.ingest(*args, **kwargs)
        logging.debug('Loaded %s %s', site, source)
        if source not in self.data_dict[site]:
            self.data_dict[site].append(source)

    def ingestAll(self, read_vars='all'):
        """Ingest time series for all sites and sources"""
        # Ingest all entries in the models section
        for category in self.cfg['sources']:
            for source in self.cfg['sources'][category]:
                try:
                    tshift = self.cfg['tshifts'][source.lower()]
                except KeyError:
                    tshift = None
                for site in self.cfg['sites']['sites']:
                    infile = \
                        self.cfg['filetemplates'][category+'_file_template'].\
                        format(site=site, model=source)
                    self.ingest(site, source, infile, read_vars=read_vars,
                                tshift=tshift)

        # Ingest all the observations
        for category in self.cfg['observations']['observations']:
            for site in self.cfg['sites']['sites']:
                infile = self.cfg['filetemplates'][category+'_file_template'].\
                             format(site=site)
                self.ingest(site, category, infile, read_vars=read_vars)

    @classmethod
    def restore(cls, path):
        """Unpickle the class instance. The data has to be restored separately
           after this with restore_data. The sequence is
           p = PlumberAnalysis.restore(path); p.restore_data(path)
           This is not all bad, it means you can read pickled data from another
           source than your class instance"""
        pfile = os.path.join(path, 'class_instance.pickle')
        with open(pfile, 'rb') as f:
            return pickle.load(f)

    def restoreData(self, path):
        """Unpickle the data for all sites and sources"""
        # pickle self.data as separate files. Since we do not restore data
        # by default, we loop over the data_dict
        self.data = {}
        for site in self.data_dict:
            for source in self.data_dict[site]:
                self.restoreDataAtom(path, site, source)

    def restoreDataAtom(self, path, site, source):
        """Unpickle the data for a single site and source"""
        if site not in self.data:
            self.data[site] = {}
        pfile = os.path.join(path, '{}_{}.pickle'.format(site, source))
        with open(pfile, 'rb') as f:
            self.data[site][source] = pickle.load(f)
        if site not in self.data_dict:
            self.data_dict[site] = {}
        if source not in self.data_dict[site]:
            self.data_dict[site].append(source)

    def store(self, path):
        """Pickle the class instance. Note that self.data is pickled separately
           from the class, to avoid large file size bug in python 3. All pickle
           files will be placed in path, which will be created if it does not
           exist. If it already exists, then any files in path will be
           overwritten."""
        # Create path
        try:
            os.makedirs(path)
        except os.error:
            pass
        # pickle the class instance
        pfile = os.path.join(path, 'class_instance.pickle')
        with open(pfile, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        # pickle self.data as separate files
        for site in self.data:
            for source in self.data[site]:
                pfile = os.path.join(path, '{}_{}.pickle'.format(site, source))
                with open(pfile, 'wb') as f:
                    pickle.dump(self.data[site][source], f,
                                pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    # get configuration file from command-line
    try:
        configfile = sys.argv[1]
    except IndexError:
        sys.exit('Usage: {} <configuration file>'.format(sys.argv[0]))

    # parse configuration file to get logging info
    cfgparser = \
        configparser.ConfigParser(allow_no_value=True,
                                  interpolation=configparser.
                                  ExtendedInterpolation())
    cfgparser.optionxform = str  # preserve case of configuration keys
    cfgparser.read(configfile)

    # initiate logging - note that cfgparser.get() returns None when the entry
    # does not exist
    logfile = cfgparser.get('LOGGING', 'logfile')
    if logfile:
        try:
            loglevel = cfgparser.get('LOGGING', 'loglevel').upper()
        except AttributeError:
            loglevel = loglevel_default.upper()
        loglevel = getattr(logging, loglevel)
        logging.basicConfig(filename=logfile, filemode='w', level=loglevel)
        logging.debug('Initiated logging to logfile %s', logfile)
    else:
        logger = logging.getLogger()
        logger.disabled = True

    b = PlumberAnalysis(configfile)

    # Shutdown logging (last act)
    logging.shutdown()
