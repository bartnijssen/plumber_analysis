import plumber.plumber as pl
configfile = '/Users/nijssen/Dropbox/data/PLUMBER/test/plumber.config'
b = pl.PlumberAnalysis(configfile)
b.ingestall()
ppath = '/Users/nijssen/Dropbox/data/PLUMBER/PLUMBER_data/pickle'
b.store(ppath)
