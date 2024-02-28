import os
import numpy as np
import pandas as pd
import argparse
import json

from datetime import datetime
from utils.data import write_anon, read_raw_fromdf, dump_anon

from utils.types import AnonMethod
from clustering_based.anonymizer import get_result_one as cb_get_result_one

from basic_mondrian.anonymizer import get_result_one
from basic_mondrian.utils.read_adult_data import read_tree

from datasets.categorical import DATASET_ATTRIBUTES_DICT

def main(conf):
    anon_method = conf['algo_conf']['algo']
    k = conf['algo_conf']['k']
    dataset = conf['dataset']
    batch_size = conf['dataset_conf']['batch_size']
    attrs = conf['dataset_conf']['attrs']

    # define necessary paths

    # Data path
    path = os.path.join('datasets', dataset, '')  # trailing /
    # Dataset path
    data_path = os.path.join(path, f'{dataset}.csv')
    # Generalization hierarchies path
    gen_path = os.path.join('generalization', 'hierarchies', dataset, '')  # trailing /

    # load the data
    if dataset == 'diabetes':
        data = pd.read_csv(os.path.join(path, f'diabetes_prediction_dataset.csv'),delimiter=',')
    else:
        data = pd.read_csv(data_path, delimiter=';')
    if dataset == "adult":
        data = data.drop(labels=["ID"], axis="columns")
    print(
        'Original Data: ' + str(data.shape[0]) + ' entries, ' + str(data.shape[1]) + ' attributes')
    # Get batch
    if batch_size > 0:
        np.random.seed(30)
        #rand_idx = np.random.randint(data.shape[0], size=batch_size)
        #data = data.iloc[rand_idx, :]
        data = data.sample(n=batch_size, replace=False)
    # Get the specific columns
    if attrs:
        data = data[attrs]
    print(f'Batch to process: {data.shape[0]} users, {data.shape[1]} attributes')


    # Create necessary fields
    ATT_NAMES = list(data.columns)
    print(ATT_NAMES)
    ATTRIBUTES_DICT = DATASET_ATTRIBUTES_DICT[dataset]
    QI_INDEX = [i for i,attr in enumerate(ATT_NAMES) if ATTRIBUTES_DICT[attr][0]]
    IS_CAT = [ATTRIBUTES_DICT[ATT_NAMES[idx]][1] for idx in QI_INDEX]
    SA_INDEX = [index for index in range(len(ATT_NAMES)) if index not in QI_INDEX]

    QI_NAMES = list(np.array(ATT_NAMES)[QI_INDEX])
    SA_var = [ATT_NAMES[i] for i in SA_INDEX]

    # folder for all results
    res_folder = os.path.join('results', dataset, anon_method, str(len(data)), str(k),
                              datetime.utcnow().isoformat().replace(':', '_'))
    # path for anonymized datasets
    anon_folder = os.path.join(res_folder, 'anon_dataset', '')  # trailing /
    # path for pickled numeric values
    numeric_folder = os.path.join(res_folder, 'numeric')

    # create path needed for results recursively
    os.makedirs(anon_folder)
    os.makedirs(numeric_folder)

    raw_data, header = read_raw_fromdf(data, numeric_folder, dataset, QI_INDEX, IS_CAT)
    #raw_data, header = read_raw(path, numeric_folder, dataset, QI_INDEX, IS_CAT)

    ATT_TREES = read_tree(gen_path, numeric_folder, dataset, ATT_NAMES, QI_INDEX, IS_CAT)
    anon_data, data_util, run_time = None, None, None
    s = 0
    s_folder = os.path.join(anon_folder, 's_' + str(s))
    os.mkdir(s_folder)
    data.to_csv(os.path.join(s_folder, f'{dataset}_batch_data.csv'), index=False)
    rnd = 36
    np.random.seed(rnd)
    if anon_method == AnonMethod.MONDRIAN:
        anon_data, data_util, run_time,  = get_result_one(ATT_TREES, raw_data, k, path, QI_INDEX, SA_INDEX)
    elif anon_method == 'oka':
        anon_data, data_util, run_time,  = cb_get_result_one(ATT_TREES, raw_data, k, path, QI_INDEX, SA_INDEX, 'oka')
    elif anon_method == 'kmember':
        anon_data, data_util, run_time,  = cb_get_result_one(ATT_TREES, raw_data, k, path, QI_INDEX, SA_INDEX, 'kmember')
    elif anon_method == 'knn':
        anon_data, data_util, run_time, = cb_get_result_one(ATT_TREES, raw_data, k, path, QI_INDEX,
                                                            SA_INDEX, 'knn')

    # Write anonymized data in csv file
    nodes_count = write_anon(s_folder, anon_data, header, k, s, dataset)
    #dump_anon(s_folder, anon_data, header,dataset, ATT_NAMES, QI_INDEX, SA_INDEX)
    res = f"{anon_method},{batch_size},{k},{len(QI_INDEX)},{data_util},{run_time}"
    return res



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    with open(args.filename) as f:
        conf_list = json.load(f)
    results = []
    for k in conf_list['algo_conf']['k']:
        if k < 2:
            print("invalid k value")
            exit(1)
        for algo in conf_list['algo_conf']['algo']:
            for batch_size in conf_list['dataset_conf']['batch_size']:
                for attrs in conf_list['dataset_conf']['attrs']:
                    conf = {
                        "dataset": conf_list['dataset'],
                        "algo_conf": {
                            "k": k,
                            "algo": algo
                        },
                        "dataset_conf": {
                            "batch_size": batch_size,
                            "attrs": attrs,
                        }
                    }
                    res = main(conf)
                    results.append(res)
    print(f"Algorithm,BatchSize,k,n_att,ncp,run_time")
    for res in results:
        print(res)


