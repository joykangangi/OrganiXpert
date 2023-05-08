# Helper function to preprocess data from the web application before making inference
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

def preprocess_before_inference(data):
    data = pd.DataFrame(data, columns=['Soil_type', 'crop',  'nitrogen', 'potassium', 'phosphorus'])
    le = LabelEncoder()
    data['Soil_type'] = le.fit_transform(data['Soil_type'])
    data['crop'] = le.fit_transform(data['crop'])
    scaler = MinMaxScaler()
    # Normalize N, P and K values to be between 0 and 1
    data[['nitrogen', 'potassium', 'phosphorus']] = scaler.fit_transform(data[['nitrogen', 'potassium', 'phosphorus']])
    return data





    