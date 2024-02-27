import helper_functions
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


colors = {'Original Dataset': 'g', 'Only K-Anonymity': 'r', 'Random Deletion (average)': 'b'}


def prepr(df, numericals):
    return df[numericals].apply(lambda x:
                                x.apply(lambda y:
                                        pd.Interval(left=float(y.split(',')[0]),
                                                    right=float(y.split(',')[1]), closed='both')),
                                axis=1)


def converter(x):
    try:
        return float(x)
    except ValueError:
        spl = x.split('-')
        return pd.Interval(float(spl[0]), float(spl[1]), closed='left')


def get_group(x, b):
    if x == '*':
        return x
    for val in b:
        if converter(x) in val:
            return val
    return None

def gen_stats_series(df, qid, sa, xs):
    grps = None
    grp_idx = [
        qid if qid == 'gender' else lambda idx: get_group(df[qid].loc[idx], xs),
    ]
    match sa:
        case 'diabetes' | 'hypertension' | 'heart_disease' | 'smoking_history':
            grp_idx.append(sa)
            return df[[qid,sa]].groupby(grp_idx).size()
        case 'HbA1c_level' | 'blood_glucose_level':
            return df[[qid,sa]].groupby(grp_idx).agg({sa: 'mean'})

def gen_stats_table(dfs, qid, sa, xs):
    stats = pd.DataFrame()
    for k, df in dfs.items():
        ser = gen_stats_series(df, qid, sa, xs)
        stats[k] = ser
    return stats


def draw_plot(d, ax, x_ticks):
    x = np.arange(len(x_ticks))
    width = 0.15
    multiplier = 0
    ax.set_xticks(x + width, x_ticks)
    for attribute, measurement in d.items():
        if attribute == 'Original Dataset' or attribute == 'Only K-Anonymity' or attribute == 'Random Deletion (average)':
            # print(measurement)
            offset = width * multiplier
            ax.plot(x + offset, measurement, width, color=colors[attribute], marker='.')
            ax.bar(x + offset, measurement, width, label=attribute, color=colors[attribute],
                   alpha=0.35)
            # ax.bar_label(rects, padding=3)
            multiplier += 1
    ax.legend(loc='upper center', ncols=3)


def gen_plot(ylabel, qid, title, pt, path, qid_ticks, save=False):
    sns.set_theme()
    fig, ax = plt.subplots(layout='constrained')
    fig.set_figwidth(10)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(qid)
    ax.set_title(title)
    x_ticks = qid_ticks[qid]
    draw_plot(pt, ax, x_ticks)
    ax.set_ylim(0, ax.get_ylim()[1] + 0.3 * ax.get_ylim()[1])
    plt.show()
    if save:
        plt.savefig(path)
        plt.close()

def test(dfs, qid, sa, qid_ticks, sa_ticks, sa_categorical, save=False):
    stats = gen_stats_table(dfs, qid, sa, qid_ticks[qid])
    stats['Random Deletion (average)'] = stats.iloc[:, 2:].mean(axis=1)
    stats = stats.fillna(0)
    if sa_categorical:
        stats.rename_axis([qid, sa], inplace=True)
        for qidval in qid_ticks[qid]:
            for saval in sa_ticks[sa]:
                if (qidval, saval) in stats.index:
                    pass
                else:
                    print(qidval, saval)
                    stats.loc[pd.IndexSlice[qidval, saval], :] = 0
        # Only for categorical SAs
        # Convert count to percentage
        # for xtick in qid_ticks[qid]:
        #     stats.loc[pd.IndexSlice[xtick,:],:] = stats.loc[pd.IndexSlice[xtick,:],:].apply(lambda x: x*100/x.sum())
        stats_arr = {}
        # Partition the table for plotting
        for val in sa_ticks[sa]:
            stats_arr[val] = (stats.loc[(slice(None), val), :])
        # Categorical SAs
        for sa_val in sa_ticks[sa]:
            # sa_val = sa_ticks[sa][cidx]
            pt = stats_arr[sa_val].copy()
            # display(pt.T)
            # pt.loc[pd.IndexSlice[qid_ticks[qid][0],1],:] = 0
            pt = pt.loc[pd.IndexSlice[qid_ticks[qid], :], :]
            ylabel = f'Number of people with {sa}={sa_val}'
            title = f'Number of people with {sa}={sa_val} by {qid}'
            #figpath = os.path.join(result_path, qid, sa, f"{qid}_{sa}_{sa_val}.png")
            #gen_plot(ylabel, qid, title, pt, None, qid_ticks, save=save)

    else:
        stats.rename_axis(qid, inplace=True)
        # Numerical SAs
        pt = stats.copy()
        # pt.loc[qid_ticks[qid][0],:] = 0
        pt = pt.loc[qid_ticks[qid], :]
        # display(pt)
        ylabel = f'Average {sa}'
        title = f'Average {sa} by {qid}'
        #figpath = os.path.join(result_path, qid, sa, f"{qid}_{sa}.png")
        #gen_plot(ylabel, qid, title, pt, None, qid_ticks, save=save)
    return stats



