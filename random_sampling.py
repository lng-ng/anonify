import numpy as np
import pandas as pd
import os
import time
import argparse
import json
from datetime import datetime

def random_deletion(df, p, qids):
    grp = df.groupby(qids)
    labels = grp.apply(lambda x: x.index)
    result = df.copy()
    for label in labels:
        arr = label.to_numpy()
        drop_idx = np.random.choice(arr, size=int(p*len(label)), replace=False)
        result = result.drop(drop_idx)
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    with open(args.filename) as f:
        conf = json.load(f)
    dataset_id = conf['id']
    print(f"ID: {dataset_id}")
    inp = conf['input']
    p = conf['sampling_percentage']
    n = conf['num_experiments']
    qids = conf['qids']
    df = pd.read_csv(inp, sep=",")
    save_path = os.path.join(datetime.utcnow().isoformat().replace(':', '_'))
    runtimes = []
    os.makedirs(save_path)
    for i in range(n):
        t = time.time()
        res_df = random_deletion(df, p, qids)
        t = time.time() - t
        runtimes.append(t)
        res_df.to_csv(os.path.join(save_path, f'{dataset_id}_sampled_p{int(p*100)}_t{i}.csv'),index=False)

    print(f"iteration,sampling_percentage,run_time")
    for i, t in enumerate(runtimes):
        print(i, p, t)