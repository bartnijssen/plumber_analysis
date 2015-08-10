import plumber.plumber as pl
import pickle

ppath = '/Users/nijssen/Dropbox/data/PLUMBER/PLUMBER_data/pickle'
p = pl.PlumberAnalysis.restore(ppath)
p.restore_data(ppath)
