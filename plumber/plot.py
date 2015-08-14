"""
Plotting functions for plumber
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from . import io
from . import fargs
from . utils import flatten
callme = fargs.callFuncBasedOnDict


def setPlotDefaults(plotdict):
    """Set plot defaults based on plotdict"""
    if plotdict is None or not plotdict:
        return
    for key, val in plotdict.items():
        # mpl.rcParams.update({key: val})
        mpl.rcParams[key] = val


def setupPlotGrid(nrows, ncols, sharex='all', sharey='all', squeeze=None,
                  subplot_kw=None, *args, **kwargs):
    """Setup the plotting grid for a plot with nrows x ncols panels"""
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, sharex=sharex,
                           sharey=sharey, squeeze=squeeze,
                           subplot_kw=subplot_kw, *args, **kwargs)
    return (fig, ax)


class Plot(object):
    """Base class for plotting. This just sets up the overall plot. Each plot
       consists of one or more panels, """

    def __init__(self, plotdict):
        """Initialize Plot instance based on a dictionary with plot info."""
        if plotdict is None or plotdict is not type(dict):
            raise ValueError
        else:
            self.plotdict = plotdict
        self.fig, self.ax = plt.subplots(**self.plotdict['figure'])

    @classmethod
    def fromConfigFile(cls, configfile, section):
        """Initialize Plot Instance based on a configuration file. The section
           indicates the section in the configuration file to read"""
        cfg = io.parseConfig(configfile)
        return cls(cfg[section])


def plot_mean_diurnal_by_site_single_var(p, section, **kwargs):
    """Plot the mean diurnal cycle by site for selected models

    Parameters
    ----------
    Required:
        p : PlumberAnalysis instance
        section : key for p.cfg that has info that is specific to this plot,
                  i.e. p.cfg[section]

    Returns
    -------
    fig : matplotlib Figure instance
    """

    try:
        setPlotDefaults(p.cfg['plot_defaults'])
    except KeyError:
        pass
    info = p.cfg[section]

    try:
        info['figsize'] = (info['figwidth'], info['figheight'])
    except KeyError:
        info['figsize'] = mpl.rcParams['figure.figsize']

    fig, axes = callme(plt.subplots, info, squeeze=False,
                       figsize=info['figsize'], **kwargs)
    iterax = iter(flatten(axes))

    sites = sorted(p.data)
    for site in sites:
        ax = next(iterax)
        for source in p.data[site]:
            df = p.data[site][source]
            df[info['read_vars']].\
                groupby(lambda x: x.hour +
                        x.minute/60).mean().plot(ax=ax, label=source)
            ax.legend().set_visible(False)

    for i in range(axes.shape[0]):
        callme(axes[i][0].set_ylabel, info, **kwargs)
    for i in range(axes.shape[1]):
        callme(axes[-1][i].set_xlabel, info, **kwargs)

    iterax = iter(flatten(axes))
    for site in sites:
        ax = next(iterax)
        ax.text(0.05, 0.95, site, horizontalalignment='left',
                verticalalignment='top', transform=ax.transAxes)

    ax = axes[0][0]
    try:
        ax.legend().set_visible(info['legend'])
    except:
        pass

    ax.text(0.05, 0.85, info['read_vars'], horizontalalignment='left',
            verticalalignment='top', transform=ax.transAxes)

    fig.tight_layout()
    callme(fig.savefig, info, filename=info['plotfilename'], **kwargs)

plotlib = [plot_mean_diurnal_by_site_single_var]
