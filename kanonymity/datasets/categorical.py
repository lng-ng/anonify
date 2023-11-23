
# [is_quasi_identifier, is_categorical]
ADULT_ATTRIBUTES = {
    'sex': [True, True],
    'age': [True, False],
    'race': [True, True],
    'marital-status': [True, True],
    'education': [True, True],
    'native-country': [True, True],
    'workclass': [True, True],
    'occupation': [True, True],
    'salary-class': [False],
    'ID': [False]
}

DIABETES_ATTRIBUTES = {
    'gender': [True, True],
    'age': [True, True],
    'hypertension': [False, True],
    'heart_disease': [False, True],
    'smoking_history': [False, True],
    'bmi': [True, True],
    'HbA1c_level': [False],
    'blood_glucose_level': [False],
    'diabetes': [False],
    'RID': [False]
}

DATASET_ATTRIBUTES_DICT = {
    'adult': ADULT_ATTRIBUTES,
    'diabetes': DIABETES_ATTRIBUTES
}
