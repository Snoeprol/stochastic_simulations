"""
=============================================
Discrete distribution as horizontal bar chart
=============================================

Stacked bar charts can be used to visualize discrete distributions.

This example visualizes the result of a survey in which people could rate
their agreement to questions on a five-element scale.

The horizontal stacking is achieved by calling `~.Axes.barh()` for each
category and passing the starting point as the cumulative sum of the
already drawn bars via the parameter ``left``.
"""
from queue_with_dist import *
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 22})

SHORTEST = False
n = 15
queue = Queue(0,1/4, 1, 3.5, n, False)
queue.process_customers()

data = np.zeros((n, 3))

for i, customer in enumerate(queue.customers):
    data[i][0] = customer.arrival_time
    data[i][1] = customer.time_used
    data[i][2] = customer.process_time

labels = ['Customer ' + str(customer.id) for customer in queue.customers]


category_names = ['', 'Queue time',
                  'Service time', 'Agree', 'Strongly agree']



def survey(results, category_names):
    """
    Parameters
    ----------
    results : dict
        A mapping from question labels to a list of answers per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*.
    category_names : list of str
        The category labels.
    """
    data_cum = data.cumsum(axis=1)
    category_colors = plt.get_cmap('RdYlGn')(
        np.linspace(0.15, 0.85, data.shape[1]))
    category_colors_2 = category_colors
    category_colors_2[0] = 0
    category_colors_2[1] = [1.0, 0.0, 0.0,1]
    category_colors_2[2] = [0.0, 1.0, 0.0,1]
    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    #ax.xaxis.set_visible(False)
    ax.vlines(np.linspace(0, queue.time, 10), 0, n + 5, ls = '-.')
    print(category_colors_2)
    for i, (colname, color) in enumerate(zip(category_names, category_colors_2)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=1,
                label=colname, color=color)
        xcenters = starts + widths / 2

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        for y, (x, c) in enumerate(zip(xcenters, widths)):
            if c > 0.2:
                ax.text(x, y, str(round(c, 1)), ha='center', va='center',
                        color=text_color)
    ax.set_xticks(np.round(np.linspace(0, queue.time, 10), decimals = 2)) 
    ax.set_xlabel('Time')
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')

    return fig, ax

survey(data, category_names)
plt.show()

#############################################################################
#
# ------------
#
# References
# """"""""""
#
# The use of the following functions, methods, classes and modules is shown
# in this example:

import matplotlib
matplotlib.axes.Axes.barh
matplotlib.pyplot.barh
matplotlib.axes.Axes.text
matplotlib.pyplot.text
matplotlib.axes.Axes.legend
matplotlib.pyplot.legend
