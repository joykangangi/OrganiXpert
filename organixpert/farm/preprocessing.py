# Helper function to preprocess data from the web application before making inference
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler

def preprocess_before_inference(data):
    le = LabelEncoder()
    data[:, 0:2] = le.fit_transform(data[:, 0:2])
    scaler = MinMaxScaler()
    # Normalize N, P and K values to be between 0 and 1
    data[:, 2] = scaler.fit_transform(data[:, 2])
    return data