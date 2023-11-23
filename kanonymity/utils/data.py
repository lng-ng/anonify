# -*- coding: utf-8 -*-

import csv
import os
import pickle
import jsbeautifier
import json
import numpy as np

def read_raw_fromdf(df, numeric_path, dataset, qi_index, is_cat, sort_count=False):
    numeric_dict = [df.astype(str).iloc[:,idx].value_counts(ascending=True).to_dict() if not cat
                    else {} for idx, cat in zip(qi_index, is_cat)]
    data = df.to_numpy().astype(str).tolist()
    header = df.columns.to_numpy().astype(str).tolist()
    #print(numeric_dict)
    for i, qii, cat in zip(range(len(qi_index)), qi_index, is_cat):
        if not cat:
            with open(os.path.join(numeric_path, dataset + '_' + header[qii] + '_static.pickle'),
                      'wb') as static_file:
                sort_value = None
                if sort_count:
                    sort_value = [elem[0] for elem in
                                  sorted(numeric_dict[i].items(), key=lambda x: float(x[1]))]
                else:
                    sort_value = sorted(numeric_dict[i].keys(), key=lambda x: float(x))
                pickle.dump((numeric_dict[i], sort_value), static_file)
    return (data,header)


def read_raw(path, numeric_path, dataset, qi_index, is_cat, delimiter=';', sort_count=False):
    """Reads dataset from a csv file. Split in header and data

        :param file_path: Path to the csv file
        :param delimiter: Character that is used as delimiter in the csv file
        :return: 2d list: data[col][row], list: header[col]
    """
    numeric_dict = [{} for elem in qi_index]
    data = []
    with open(os.path.join(path, f'{dataset}.csv')) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimiter)
        header = next(csv_reader)

        for row in csv_reader:
            data.append(row)
            # save the count of each value
            for i, qii, cat in zip(range(len(qi_index)), qi_index, is_cat):
                if not cat:
                    try:
                        numeric_dict[i][row[qii]] += 1
                    except KeyError:
                        numeric_dict[i][row[qii]] = 1

        # sort non categorical value by count or value
        for i, qii, cat in zip(range(len(qi_index)), qi_index, is_cat):
            if not cat:
                with open(os.path.join(numeric_path, dataset + '_' + header[qii] + '_static.pickle'), 'wb') as static_file:
                    sort_value = None
                    if sort_count:
                        sort_value = [elem[0] for elem in sorted(numeric_dict[i].items(), key=lambda x: x[1])]
                    else:
                        sort_value = sorted(numeric_dict[i])
                    pickle.dump((numeric_dict[i], sort_value), static_file)
    return (data, header)


def reorder_columns(data, qi_index):
    res = []
    for row in data:
        qi = [elem for i, elem in enumerate(row) if i in qi_index]
        non_qi = [elem for i, elem in enumerate(row) if i not in qi_index]
        res.append([*qi, *non_qi])
    return res


def restore_column_order(data, qi_index):
    res = []
    for row in data:
        new_row = row[len(qi_index):]
        for i, elem in zip(qi_index, row[:len(qi_index)]):
            new_row.insert(i, elem)
        res.append(new_row)
    return res


def transform_columns(data):
    res = [[] for _ in range(len(data[0]))]
    for row in data:
        print(row)
        for i, column in enumerate(row):
            print(column)
            res[i].append(column)
    return res


def write_anon(path, anon_data, header, k, s, dataset, delimiter=';'):
    if isinstance(anon_data, dict):
        anon_data = anon_data.values()
    else:
        anon_data = [anon_data]
    for i, data in enumerate(anon_data):
        with open(os.path.join(path, dataset + "_anonymized_" + str(k) + '_' + str(i) + ".csv"), mode='w', newline='') as anon_file:
            anon_writer = csv.writer(anon_file, delimiter=delimiter)
            anon_writer.writerow(header)
            anon_writer.writerows(data)
    return len(anon_data)

def save_json(data, data_path):
    options = jsbeautifier.default_options()
    options.indent_size = 4
    with open(data_path, "w") as f:
        res = jsbeautifier.beautify(json.dumps(data), options)
        f.write(res)

def dump_anon(path, anon_data, header, dataset, att_names, qid_idx, sa_idx):
    new_qids = None
    grp = []
    grp_size = []
    grp_sa = []
    for row in anon_data:
        qids = np.array(row)[qid_idx]
        if new_qids is None or (qids != new_qids).any():
            new_qids = qids
            grp.append(new_qids.tolist())
            grp_size.append(0)
            dct = {}
            for idx in sa_idx:
                dct[att_names[idx]] = []
            grp_sa.append(dct)
        grp_size[-1] += 1
        for idx in sa_idx:
            grp_sa[-1][att_names[idx]].append(row[idx])
    output = {
        'header': header,
        'grp': [
            {
                'label': grp,
                'size': size,
                'sa': sa
            } for grp, size, sa in zip(grp, grp_size, grp_sa)
        ]
    }
    save_json(output, os.path.join(path, f"{dataset}_anonymized_group.json"))

