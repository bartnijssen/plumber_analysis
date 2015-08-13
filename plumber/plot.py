"""
Plotting functions for plumber
"""
import matplotlib.pyplot as plt
from . import io
from . import fargs


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


def plot_a(p, section, *args, **kwargs):
    """Plot an a

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
    info = p.cfg[section]
    func_args = fargs.selectArgsFromDict(plt.subplots, info)
    fig, ax = plt.subplots(*func_args)


plotlib = [plot_a]
