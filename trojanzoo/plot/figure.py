# -*- coding: utf-8 -*-

from trojanzoo.utils import to_numpy, arctanh
from .font import palatino, palatino_bold

import os
import numpy as np
import torch

from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import seaborn


class Figure:
    def __init__(self, name, path=None, fig=None, ax=None):
        super(Figure, self).__init__()
        self.name = name
        self.path = path
        if path is None:
            self.path = './output/'
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.fig = fig
        self.ax = ax
        if fig is None and ax is None:
            self.fig, self.ax = plt.subplots(1, 1, figsize=(5, 3.75))
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['bottom'].set_visible(True)
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.grid(axis='y', linewidth=1)

        self.ax.set_xlim([0.0, 1.0])
        self.ax.set_ylim([0.0, 1.0])

    def set_legend(self, frameon=False, prop=palatino_bold, fontsize=13, **kwargs):
        self.ax.legend(prop=prop, frameon=frameon, **kwargs)
        plt.setp(self.ax.get_legend().get_texts(), fontsize=fontsize)

    def set_axis_label(self, axis, text, fontproperties=palatino_bold, fontsize=16):
        if axis == 'x':
            func = self.ax.set_xlabel
        elif axis == 'y':
            func = self.ax.set_ylabel
        else:
            raise ValueError('Argument \"axis\" need to be \"x\" or \"y\"')
        func(text, fontproperties=fontproperties, fontsize=fontsize)

    def set_title(self, text=None, fontproperties=palatino_bold, fontsize=16):
        if text is None:
            text = self.name
        self.ax.set_title(
            text, fontproperties=fontproperties, fontsize=fontsize)

    def save(self, path=None):
        if path is None:
            path = self.path
        self.fig.savefig(path+self.name+'.svg', dpi=100, bbox_inches='tight')

    def set_axis_lim(self, axis, lim=[0.0, 1.0], margin=[0.0, 0.0], piece=10, _format='%.1f', fontproperties=palatino, fontsize=13):
        if _format == 'integer':
            _format = '%d'

        if axis == 'x':
            lim_func = self.ax.set_xlim
            ticks_func = self.ax.set_xticks

            def format_func(_str):
                self.ax.xaxis.set_major_formatter(
                    ticker.FormatStrFormatter(_str))
        elif axis == 'y':
            lim_func = self.ax.set_ylim
            ticks_func = self.ax.set_yticks

            def format_func(_str):
                self.ax.yaxis.set_major_formatter(
                    ticker.FormatStrFormatter(_str))
        else:
            raise ValueError('Argument \"axis\" need to be \"x\" or \"y\"')

        ticks = np.append(
            np.arange(lim[0], lim[1], (lim[1]-lim[0])/piece), lim[1])
        final_lim = [lim[0]-margin[0], lim[1]+margin[1]]
        lim_func(final_lim)
        ticks_func(ticks)

        if axis == 'x':
            self.ax.set_xticklabels(self.ax.get_xticks(),
                                    fontproperties=fontproperties, fontsize=fontsize)
        elif axis == 'y':
            self.ax.set_yticklabels(self.ax.get_yticks(),
                                    fontproperties=fontproperties, fontsize=fontsize)
        format_func(_format)

    def bar(self, x, y, color='black', width=0.2, align='edge', edgecolor='white', label=None, **kwargs):
        # facecolor edgewidth alpha
        return self.ax.bar(x, y, color=color, width=width, align=align, edgecolor=edgecolor, label=label, **kwargs)

    def autolabel(self, rects, above=True, fontproperties=palatino, fontsize=6):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = int(rect.get_height())
            offset = 3 if above else -13
            self.ax.annotate('%d' % (abs(height)),
                             xy=(rect.get_x() + rect.get_width() / 2, height),
                             xytext=(0, offset),  # 3 points vertical offset
                             textcoords="offset points",
                             ha='center', va='bottom', fontproperties=fontproperties, fontsize=fontsize)

    def curve(self, x, y, color='black', linewidth=2, label=None, markerfacecolor='white', linestyle='-', zorder=1, **kwargs):
        # linestyle marker markeredgecolor markeredgewidth markerfacecolor markersize alpha
        ax = seaborn.lineplot(x, y, ax=self.ax, color=color, linewidth=linewidth,
                              label=label, markerfacecolor=markerfacecolor, zorder=zorder, **kwargs)
        line = ax.get_lines()[-1]
        line.set_linestyle(linestyle)
        return line

    def scatter(self, x, y, color='black', marker='D', linewidth=2, facecolor='white', zorder=3, **kwargs):
        # marker markeredgecolor markeredgewidth markerfacecolor markersize alpha
        return self.ax.scatter(x, y, color=color, marker=marker, linewidth=linewidth, facecolor=facecolor, zorder=zorder, **kwargs)

# Markers
# '.' point marker
# ',' pixel marker
# 'o' circle marker
# 'v' triangle_down marker
# '^' triangle_up marker
# '<' triangle_left marker
# '>' triangle_right marker
# '1' tri_down marker
# '2' tri_up marker
# '3' tri_left marker
# '4' tri_right marker
# 's' square marker
# 'p' pentagon marker
# '*' star marker
# 'h' hexagon1 marker
# 'H' hexagon2 marker
# '+' plus marker
# 'x' x marker
# 'D' diamond marker
# 'd' thin_diamond marker
# '|' vline marker
# '_' hline marker

# Line Styles
# '-'     solid line style
# '--'    dashed line style
# '-.'    dash-dot line style
# ':'     dotted line style

    @staticmethod
    def get_roc_curve(label, pred, threshold_num=30000):

        total_inst = len(label)
        total_pos_inst = len(np.where(label == 1)[0])

        assert len(label) == len(pred)
        # true positive rates and false positive rates
        tprs, fprs, thresholds = [], [], []

        # iterate over all positive thresholds
        for threshold in np.unique(pred):

            pred_pos_idx = np.where(pred >= threshold)[0]

            # number of predicted positive instances
            pred_pos_inst = len(pred_pos_idx)
            # number of true positive instances
            true_pos_inst = np.count_nonzero(label[pred_pos_idx])

            tpr = true_pos_inst*1. / total_pos_inst*1.
            fpr = (pred_pos_inst-true_pos_inst) * \
                1. / (total_inst-total_pos_inst)*1.
            tprs.append(tpr)
            fprs.append(fpr)
            thresholds.append(threshold)

        return fprs, tprs, thresholds

    @staticmethod
    def sort(x, y):
        idx = np.argsort(x)
        return np.array(x)[idx], np.array(y)[idx]

    @staticmethod
    def normalize(x, _min=None, _max=None, tgt_min=0.0, tgt_max=1.0):
        x = to_numpy(x)
        if _min is None:
            _min = x.min()
        if _max is None:
            _max = x.max()
        x = (x - _min)/(_max-_min) * (tgt_max-tgt_min) + tgt_min
        return x

    @staticmethod
    def groups_err_bar(x, y):
        y_dict = {}
        for _x in set(x):
            y_dict[_x] = np.array([y[t] for t in range(len(y)) if x[t] == _x])
        return y_dict

    @staticmethod
    def flatten_err_bar(y_dict):
        x = []
        y = []
        for _x in y_dict.keys():
            for _y in y_dict[_x]:
                x.append(_x)
                y.append(_y)
        return np.array(x), np.array(y)

    @classmethod
    def normalize_err_bar(cls, x, y):
        x = cls.normalize(x)
        y_dict = cls.groups_err_bar(x, y)
        y_mean = np.array([y_dict[_x].mean()
                           for _x in np.sort(list(y_dict.keys()))])
        y_norm = cls.normalize(y_mean)
        y_dict = cls.adjust_err_bar(y_dict, y_norm-y_mean)
        return cls.flatten_err_bar(y_dict)

    @classmethod
    def avg_smooth_err_bar(cls, x, y, window=3):
        y_dict = cls.groups_err_bar(x, y)
        y_mean = np.array([y_dict[_x].mean()
                           for _x in np.sort(list(y_dict.keys()))])
        y_smooth = cls.avg_smooth(y_mean, window=window)
        y_dict = cls.adjust_err_bar(y_dict, y_smooth-y_mean)
        return cls.flatten_err_bar(y_dict)

    @staticmethod
    def adjust_err_bar(y_dict, mean=None, std=None):
        sort_keys = np.sort(list(y_dict.keys()))
        if isinstance(mean, float):
            mean = mean*np.ones(len(sort_keys))
        if isinstance(std, float):
            std = std*np.ones(len(sort_keys))
        for i in range(len(sort_keys)):
            key = sort_keys[i]
            if mean:
                y_dict[key] = y_dict[key]+mean[i]
            if std:
                y_dict[key] = y_dict[key].mean() + \
                    (y_dict[key]-y_dict[key].mean())*std[i]
        return y_dict

    @staticmethod
    def avg_smooth(x, window=3):
        _x = torch.as_tensor(x)
        new_x = torch.zeros_like(_x)
        for i in range(len(_x)):
            if i < window//2:
                new_x[i] = (_x[0]*(window//2-i) +
                            _x[:i+(window+1)//2].sum())/window
            elif i >= len(_x)-(window-1)//2:
                new_x[i] = (_x[-1]*(len(_x)-1-i+(window-1)//2) +
                            _x[i-window//2:].sum())/window
            else:
                new_x[i] = _x[i-window//2:i+1+(window-1)//2].mean()
        return to_numpy(new_x) if isinstance(x, np.ndarray) else new_x

    @staticmethod
    def poly_fit(x, y, x_grid, degree=1):
        fit_data = to_numpy(y)
        z = np.polyfit(x, fit_data, degree)
        y_grid = np.polyval(z, x_grid)
        return y_grid

    @staticmethod
    def tanh_fit(x, y, x_grid, degree=1, mean_bias=0.0, scale_multiplier=1.0):
        mean = (max(y)+min(y))/2+mean_bias
        scale = max(abs(y-mean))*scale_multiplier
        fit_data = to_numpy(arctanh(torch.as_tensor((y-mean)/scale)))
        z = np.polyfit(x, fit_data, degree)
        y_grid = np.tanh(np.polyval(z, x_grid))*scale+mean
        return y_grid

    @staticmethod
    def exp_fit(x, y, x_grid, degree=1, increase=True, epsilon=0.01):
        y_max = max(y)
        y_min = min(y)
        if increase:
            fit_data = np.log(y_max+epsilon-y)
        else:
            fit_data = np.log(y+epsilon-y_min)

        z = np.polyfit(x, fit_data, degree)
        y_grid = np.exp(np.polyval(z, x_grid))
        if increase:
            y_grid = y_max+epsilon-y_grid
        else:
            y_grid += y_min-epsilon
        return y_grid

    @staticmethod
    def inverse_fit(x, y, x_grid, degree=1, y_lower_bound=0.0):
        fit_data = 1/(y-y_lower_bound)
        z = np.polyfit(x, fit_data, degree)
        y_grid = 1/(np.polyval(z, x_grid))+y_lower_bound
        return y_grid

    @staticmethod
    def monotone(x, increase=True):
        temp = 0.0
        y = np.copy(x)
        if increase:
            temp = min(x)
        else:
            temp = max(x)
        for i in range(len(x)):
            if ((increase and x[i] < temp) or (not increase and x[i] > temp)):
                y[i] = temp
            else:
                temp = x[i]
        return y
