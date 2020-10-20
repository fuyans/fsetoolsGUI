import itertools
from typing import Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def lineplot(
        x: Union[list, np.ndarray],
        y: Union[list, np.ndarray],
        legend_labels: Union[list, np.ndarray],
        acceptable_reliability: float = None,
        figsize: tuple = (3.5, 3.5),
        fig=None,
        ax=None,
        fp_figure: str = None,
        xlim: Tuple[float, float] = (15, 180),
        xlim_step: float = 15,
        n_legend_col: int = 1,
        legend_no_overlap: bool = True,
        xlabel: str = None,
        ylabel: str = None,
        plot_in_set=False,  # @param {type:"boolean"}
        plot_in_set_zoom=20,  # @param {type:"number"}
        plot_in_set_x=75,  # @param {type:"number"}
        plot_in_set_x_tol=1,  # @param {type:"number"}
        plot_in_set_y=0,  # acceptable_reliability
        plot_in_set_y_tol=0.01,  # @param {type:"number"}
):
    # Calculate the maximum time equivalence value (i.e. x-axis limit)

    # Generate x-axis array, based upon the calculated x-axis upper limit
    # x = (edges[1:] + edges[:-1]) / 2

    # Calculate the PDF and CDF of time equivalence, based upon the x-axis array

    # Generate plot
    if fig is None and ax is None:
        fig, ax = plt.subplots(1, 1, figsize=figsize, sharex=True)

    for i in range(len(y)):
        sns.lineplot(x=x[i], y=y[i], label=legend_labels[i], ax=ax, palette=sns.color_palette("husl", n_colors=20))

    if isinstance(acceptable_reliability, (float, int)):
        ax.axhline(acceptable_reliability, ls='--', c='k')
        ax.text(15, acceptable_reliability, f'{acceptable_reliability:.3f}', ha='left', va='bottom')

    # Update plot settings
    ax.grid(which='major', linestyle=':', linewidth='0.5', color='black')
    if len(legend_labels) > 1:
        if legend_no_overlap:
            ax.legend(
                shadow=False, edgecolor='k', fancybox=False, ncol=n_legend_col, fontsize='xx-small', bbox_to_anchor=(1.04, 1.018), loc="upper left"
            ).set_visible(True)
        else:
            ax.legend(shadow=False, edgecolor='k', fancybox=False, ncol=n_legend_col, fontsize='xx-small').set_visible(True)
    else:
        ax.legend().set_visible(False)
    ax.set_xticks(np.arange(xlim[0], xlim[1] + xlim_step, xlim_step))
    ax.set_xlim(*xlim)
    ax.set_yticks(np.arange(0, 1.05, 0.1))
    ax.set_ylim(-0.01, 1.01)
    ax.tick_params(axis='both', which='both', labelsize='x-small')
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)

    # plot inset
    if plot_in_set:
        from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset

        ax_ins = zoomed_inset_axes(parent_axes=ax, zoom=plot_in_set_zoom, loc=1)  # zoom-factor: 2.5, location: upper-left

        for i in range(len(y)):
            sns.lineplot(x=x, y=y[i], ax=ax_ins, palette=sns.color_palette("husl", n_colors=20))
        ax_ins.axhline(acceptable_reliability, ls='--', c='k')

        ax_ins.set_xlim(plot_in_set_x - plot_in_set_x_tol, plot_in_set_x + plot_in_set_x_tol)
        ax_ins.set_ylim(plot_in_set_y - plot_in_set_y_tol, plot_in_set_y + plot_in_set_y_tol)
        ax_ins.set_xticks([plot_in_set_x, ])
        ax_ins.set_yticks([])
        # ax_ins.xaxis.set_visible(False)
        ax_ins.yaxis.set_visible(False)
        ax_ins.legend().set_visible(False)

        mark_inset(parent_axes=ax, inset_axes=ax_ins, loc1=2, loc2=3, ec='k', fc='w', zorder=3)

    # Save plot
    if fp_figure and fig:
        fig.savefig(fp_figure, dpi=300, bbox_inches='tight', transparent=True)

    return fig, ax


def lineplot_matrix(
        dict_teq: dict,
        n_cols: int = 9,
        fp_figure: str = None,
        xlim: Tuple[float, float] = (0, 120),
        bin_width: float = 2.5,
        figsize: Tuple[float, float] = (1.2, 1.2)
):
    n_rows = int(np.ceil(len(dict_teq.keys()) / n_cols))
    figsize = (n_cols * figsize[0], n_rows * figsize[1])
    fig, axes1 = plt.subplots(n_rows, n_cols, figsize=figsize, sharex=True, sharey=True)

    try:
        axes1 = list(itertools.chain(*axes1))
    except:
        pass

    i = 0
    for k in sorted(dict_teq.keys()):
        v = dict_teq[k]
        v[v == np.inf] = np.max(v[v != np.inf])
        v[v == -np.inf] = np.min(v[v != -np.inf])

        edges = np.arange(np.min(v) - bin_width, np.max(v) + bin_width * 2, bin_width)
        centres = (edges[1:] + edges[:-1]) / 2
        hist, _ = np.histogram(v, edges, weights=np.full_like(v, 1))

        ax1 = axes1[i]
        ax2 = ax1.twinx()

        # Below is removed on 08/10/2020 due to a matplotlib error:
        # AttributeError: 'PolyCollection' object has no property 'hist'
        # sns.histplot(v, label='PDF', ax=ax2, bins=edges, kde=False, hist=True,
        #              hist_kws=dict(cumulative=False, density=True, color='grey'))
        sns.lineplot(x=centres, y=np.cumsum(hist) / len(v), ax=ax1, color='k')

        ax1.set_ylim((0, 1))
        ax1.set_yticks([0, 1])
        ax1.text(0.95, 0.5, k, transform=ax2.transAxes, ha='right', va='center')
        ax1.tick_params(axis='y', direction='in')

        ax2.set_xlabel('')
        ax2.set_yticks([])
        ax2.set_ylim(0, 0.2)
        ax2.tick_params(axis='both', direction='in')

        i = i + 1

    ax1.set_xticks(np.arange(xlim[0], xlim[1] + 1, 30))
    ax1.set_xlim(*xlim)
    fig.text(-0.01, 0.5, 'CDF [-]', ha='center', va='top', rotation=90)
    fig.text(0.5, 0, 'Equivalent of time exposure [$min$]', ha='center', va='top')

    fig.tight_layout(pad=0.1)

    if fp_figure:
        fig.savefig(fp_figure, dpi=300, bbox_inches='tight')

    return fig, axes1
