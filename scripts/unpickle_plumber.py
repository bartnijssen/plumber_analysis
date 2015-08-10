import plumber.plumber as pl
import pickle
pickle_id ='all_daf57aaa'
ppath = '/Users/nijssen/Dropbox/data/PLUMBER/plumber_analysis/pickles/{}'.\
        format(pickle_id)
p = pl.PlumberAnalysis.restore(ppath)
p.restore_data(ppath)
