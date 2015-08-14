import plumber.plumber as pl
pickle_id = 'all_daf57aaa'
configfile = \
    '/Users/nijssen/Dropbox/data/PLUMBER/'\
    'plumber_analysis/config/plumber.config'
b = pl.PlumberAnalysis(configfile)
b.ingestall()
ppath = '/Users/nijssen/Dropbox/data/PLUMBER/plumber_analysis/pickles/{}'.\
        format(pickle_id)
b.store(ppath)
