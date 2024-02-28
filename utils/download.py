import gdown
import argparse
import os

drive_ids = {
    'original': ["1Mpsr0XfQ-yAyQzarbfGEnu34Li0zVtOU", 'diabetes_prediction_dataset.csv'],
    'arx250_anonymized': ["1SRogEdk7E8REmXmt9CwpWyFF2AL_e37b", "diabetes_anonymized_arx250.csv"],
    'expr1_data': "1G-7anLLgO9bZbg7fL_dAuxHhqf_VK67Y"
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("expr", help="experiment type [infoloss | dist | ml | anon]")
    args = parser.parse_args()
    if args.expr == 'infoloss':
        gdown.download_folder(id=drive_ids['expr1_data'], quiet=True)
    elif args.expr == 'dist':
        data_folder = 'dist_data'
        os.makedirs(data_folder, exist_ok=True)
        gdown.download(id=drive_ids['original'][0], output=os.path.join(data_folder, drive_ids['original'][1]))
        gdown.download(id=drive_ids['arx250_anonymized'][0], output=os.path.join(data_folder, drive_ids['arx250_anonymized'][1]))
    elif args.expr == 'ml':
        data_folder = 'ml_data'
        os.makedirs(data_folder, exist_ok=True)
        gdown.download(id=drive_ids['original'][0], output=os.path.join(data_folder, drive_ids['original'][1]))
        gdown.download(id=drive_ids['arx250_anonymized'][0], output=os.path.join(data_folder, drive_ids['arx250_anonymized'][1]))
    elif args.expr == 'anon':
        data_folder = 'anon_data'
        os.makedirs(data_folder, exist_ok=True)
        gdown.download(id=drive_ids['arx250_anonymized'][0], output=os.path.join(data_folder, drive_ids['arx250_anonymized'][1]))
    else:
        print("Invalid argument. Experiment type can be [infoloss | dist | ml | anon]")


