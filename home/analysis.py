import pickle
import pandas as pd

def predictHumidity(year,month,day):
# load the model from a file
    with open('humidity.pickle', 'rb') as f:
        model = pickle.load(f)

    # Make predictions
    X_new = pd.DataFrame({
        'YEAR': [year],
        'MO': [month],
        'DY': [day]
    })
    y_new = model.predict(X_new)
    return y_new

def predictTemp(year,month,day):
    with open('temperature.pickle', 'rb') as f:
        model = pickle.load(f)

    # Make predictions
    X_new = pd.DataFrame({
        'YEAR': [2023],
        'MO': [5],
        'DY': [10]
    })
    y_new = model.predict(X_new)
    return y_new