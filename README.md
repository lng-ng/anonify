# Random Sampling
Sample a k-anonymized dataset. The sampled dataset has, for each equivalence class, a certain amount of random records removed.

## Requirements
For the dependencies, run ``pip install -r requirements.txt``.

## K-anonymization
The code for k-anonymization using OKA and Mondrian is provided. The implementation is based on the [open-source code](https://github.com/fhstp/k-AnonML) of Slijepčević et al. 
Run ``python anonymization.py test_conf.json`` to produce a k-anonymized dataset (either by OKA or Mondrian). The algorithm used and the value for **k** can be changed in the config file.

For the ARX algorithm, the [ARX tool](https://github.com/arx-deidentifier/arx/) is used. The ARX 250-anonymized dataset used in the evaluation is provided.

## Running the sampling code
Run ``python main.py conf.json`` to produce a sampled dataset.
Options are given in the configuration file ``conf.json``.

## About the configuration file
"input": path to the k-anonymized dataset  
"qids": the quasi-identifiers used for the k-anonymization process.  
"sampling_percentage": the percentage of records to remove from each equivalence class  
"num_experiments": number of times the sampling process will be run  
"id": affects the name of the output. The output file of the i-th run follows the naming schema {id}\_\{dataset name\}\_t\_\{i}.  

## Figures
All figures and the code to produce them are included in ``plot_figures.ipynb``.
## Python version
The sampling process was run on Python 3.11.4.


