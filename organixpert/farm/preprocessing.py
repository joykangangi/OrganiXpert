# Helper function to preprocess data from the web application before making inference
#from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

def preprocess_before_inference(data):
    data = pd.DataFrame(data, columns=['Soil_type', 'crop',  'nitrogen', 'potassium', 'phosphorus'])
    print(data)
    # le = LabelEncoder()
    # data['Soil_type'] = le.fit_transform(data['Soil_type'])
    # data['crop'] = le.fit_transform(data['crop'])
    # apply label encoding to soil type and crop columns based on how they were label encoded in the training data
    data['Soil_type'] = data['Soil_type'].map({'Sandy': 4, 'Loamy': 2, 'Clayey': 1, 'Black': 0, 'Red': 3})
    data['crop'] = data['crop'].map({'Cotton': 1, 'Groundnuts': 2, 'Maize': 3, 'Paddy': 6, 'Sugarcane': 8, 'Wheat': 10, 'Barley': 0, 'Millets': 4, 'Oil seeds': 5, 'Pulses': 7, 'Tobacco': 9})
    print(data)
    scaler = MinMaxScaler()
    # Normalize N, P and K values to be between 0 and 1
    data[['nitrogen', 'potassium', 'phosphorus']] = scaler.fit_transform(data[['nitrogen', 'potassium', 'phosphorus']])
    return data





    