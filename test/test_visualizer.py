import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import test_config as config
import pandas as pd
import matplotlib.ticker as ticker


class Visualizer:
    def __init__(self, *args, **kwargs):
        pass

    def cumulative_histogram(self, **kwargs):
        iterable = np.sort(kwargs['iterable'])
        mu = iterable[0]

        sigma = iterable[-1]
        n_bins = kwargs['n_bins']

        fig, ax = plt.subplots(figsize=config.FIGSIZE)

        # plot the cumulative histogram
        n, bins, patches = ax.hist(iterable, n_bins, density=True, histtype='step',
                                cumulative=True, label='Empirical')

        # Add a line showing the expected distribution.
        y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
            np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
        y = y.cumsum()
        y /= y[-1]

        ax.plot(bins, y, 'k--', linewidth=1.5, label='Theoretical')

        # tidy up the figure
        ax.grid(True)
        ax.legend(loc='right')
        ax.set_title('Cumulative step histograms')
        ax.set_xticks(kwargs.get('xticks'))
        ax.set_xlabel(kwargs.get('xlable'))
        ax.set_ylabel(kwargs.get('ylable'))

        plt.show()

    def date_tick_labels(self, **kwargs):
        years = sorted(kwargs['x_iterable'])
        months = kwargs.get('month')
        #yearsFmt = mdates.DateFormatter('%Y')


        fig, ax = plt.subplots()
        ax.plot(years, kwargs['y_iterable'])

        # format the ticks
        ax.xaxis.set_major_locator(ticker.FixedLocator(kwargs['x_iterable']))
        #ax.xaxis.set_major_formatter(yearsFmt)
        # ax.xaxis.set_minor_locator(months)

        # round to nearest years...
        datemin = years[0]
        datemax = years[-1] + 1
        ax.set_xlim(datemin, datemax)


        # format the coords message box
        def price(x):
            return '$%1.2f' % x
        ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
        ax.format_ydata = price
        ax.grid(True)

        # rotates and right aligns the x labels, and moves the bottom of the
        # axes up to make room for them
        #fig.autofmt_xdate()

        plt.show()
    
    def multiple_lines(self, x, *args, x_label='x label', y_label='y label'):
        with plt.style.context('Solarize_Light'):
            for y in args:
                plt.plot(x, y)
            # Number of accent colors in the color scheme
            plt.title("{} Lines".format(len(args)))
            plt.xlabel(x_label, fontsize=14)
            plt.ylabel(y_label, fontsize=14)

        plt.show()

    def one_line(self, word, x, y, x_label='x label', y_label='y label'):

        plt.plot(x, y)
        plt.title("Use of keyword {} over years".format(word))
        plt.xlabel(x_label, fontsize=14)
        plt.ylabel(y_label, fontsize=14)
        plt.savefig("godseye-plasma.png")

    def coherence(self):
        # Fixing random state for reproducibility
        np.random.seed(19680801)

        dt = 0.01
        t = np.arange(0, 30, dt)
        nse1 = np.random.randn(len(t))                 # white noise 1
        nse2 = np.random.randn(len(t))                 # white noise 2

        # Two signals with a coherent part at 10Hz and a random part
        s1 = np.sin(2 * np.pi * 10 * t) + nse1
        s2 = np.sin(2 * np.pi * 10 * t) + nse2

        fig, axs = plt.subplots(2, 1)
        axs[0].plot(t, s1, t, s2)
        axs[0].set_xlim(0, 2)
        axs[0].set_xlabel('time')
        axs[0].set_ylabel('s1 and s2')
        axs[0].grid(True)

        cxy, f = axs[1].cohere(s1, s2, 256, 1. / dt)
        axs[1].set_ylabel('coherence')

        fig.tight_layout()
        plt.show()
