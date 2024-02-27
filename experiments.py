import numpy as np
import pandas as pd
import argparse
import os
from random_sampling import random_deletion
from stats import test

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('experiment')
    args = parser.parse_args()
    load_path = os.path.join('datasets', 'diabetes_anonymized_arx250.csv')
    if args.experiment == "data_dist":
        print("Experiment: Data Distribution")
        df = pd.read_csv(load_path)
        dfo = pd.read_csv(os.path.join('datasets', 'preprocessed_diabetes.csv'))
        results = []
        p = 0.5
        qids = ['gender', 'age', 'bmi']
        ages = np.arange(0, 110, 20)
        b = []
        for i in range(len(ages) - 1):
            intv = pd.Interval(ages[i], ages[i + 1], closed='left')
            b.append(intv)
        qid_ticks = {
            'gender': ['Female', 'Male'],
            'age': b,
            'bmi': [pd.Interval(10, 30, closed='left'), pd.Interval(30, 50, closed='left')],
        }
        cat_sas = ['diabetes', 'hypertension', 'heart_disease', 'smoking_history']
        sa_ticks = {}
        for val in cat_sas:
            sa_ticks[val] = df[val].unique()
        numerical = ['HbA1c_level', 'blood_glucose_level']


        print("--Sampling the dataset 10 times--")
        for i in range(10):
            sampled_df = random_deletion(df, p, qids)
            results.append(sampled_df)

        dfs = {
            'Original Dataset': dfo,
            'Only K-Anonymity': df
        }
        for i, result in enumerate(results):
            dfs[f'Random Deletion {i}'] = result

        qid = 'age'
        sa = 'diabetes'
        test(dfs, qid, sa, qid_ticks, True, sa_ticks, save=False)

