import pandas as pd

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


def get_stats(dfs, qid, sa, qid_ticks, sa_ticks, sa_categorical):
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
                    stats.loc[pd.IndexSlice[qidval, saval], :] = 0
    else:
        stats.rename_axis(qid, inplace=True)
    return stats



