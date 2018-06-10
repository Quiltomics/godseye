import numpy as np
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
import matplotlib.cbook as cbook


class Visualizer:
    def __init__(self, *args, **kwargs):
        pass
    
    def cumulative_histogram(self):
        mu = 200
        sigma = 25
        n_bins = 50
        x = np.random.normal(mu, sigma, size=100)

        fig, ax = plt.subplots(figsize=(40, 20))

        # plot the cumulative histogram
        n, bins, patches = ax.hist(x, n_bins, density=True, histtype='step',
                                cumulative=True, label='Empirical')

        # Add a line showing the expected distribution.
        y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
            np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
        y = y.cumsum()
        y /= y[-1]

        ax.plot(bins, y, 'k--', linewidth=1.5, label='Theoretical')

        # Overlay a reversed cumulative histogram.
        ax.hist(x, bins=bins, density=True, histtype='step', cumulative=-1,
                label='Reversed emp.')

        # tidy up the figure
        ax.grid(True)
        ax.legend(loc='right')
        ax.set_title('Cumulative step histograms')
        ax.set_xlabel('Annual rainfall (mm)')
        ax.set_ylabel('Likelihood of occurrence')

        plt.show()

    def date_tick_labels(self):
        years = mdates.YearLocator()   # every year
        months = mdates.MonthLocator()  # every month
        yearsFmt = mdates.DateFormatter('%Y')

        # Load a numpy record array from yahoo csv data with fields date, open, close,
        # volume, adj_close from the mpl-data/example directory. The record array
        # stores the date as an np.datetime64 with a day unit ('D') in the date column.
        with cbook.get_sample_data('goog.npz') as datafile:
            r = np.load(datafile)['price_data'].view(np.recarray)

        fig, ax = plt.subplots()
        ax.plot(r.date, r.adj_close)

        # format the ticks
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(yearsFmt)
        ax.xaxis.set_minor_locator(months)

        # round to nearest years...
        datemin = np.datetime64(r.date[0], 'Y')
        datemax = np.datetime64(r.date[-1], 'Y') + np.timedelta64(1, 'Y')
        ax.set_xlim(datemin, datemax)


        # format the coords message box
        def price(x):
            return '$%1.2f' % x
        ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
        ax.format_ydata = price
        ax.grid(True)

        # rotates and right aligns the x labels, and moves the bottom of the
        # axes up to make room for them
        fig.autofmt_xdate()

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

    def one_line(self, x, y, x_label='x label', y_label='y label'):
        with plt.style.context('Solarize_Light'):
            plt.plot(x, y)
            plt.title("{} Lines".format(len(args)))
            plt.xlabel(x_label, fontsize=14)
            plt.ylabel(y_label, fontsize=14)
        plt.show()

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