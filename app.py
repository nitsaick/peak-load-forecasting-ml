import datetime
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

from prepare_data import prepare_data


def fit_model(data):
    workday = data[data['workday'] == 1]
    holiday = data[data['workday'] == 0]
    
    x = workday[['temperature', 'weekday']].values
    y = workday[['peak_load']].values
    workday_model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
    workday_model.fit(x, y)
    
    x = holiday[['temperature', 'holiday']].values
    y = holiday[['peak_load']].values
    holiday_model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
    holiday_model.fit(x, y)
    
    return workday_model, holiday_model


def predict(data):
    output = []
    target = []
    for _, day in data.iterrows():
        if day['workday'] == 1:
            x = day[['temperature', 'weekday']].values.reshape((1, -1))
            y = workday_model.predict(x)
        elif day['workday'] == 0:
            x = day[['temperature', 'holiday']].values.reshape((1, -1))
            y = holiday_model.predict(x)
        output.append(y.reshape((-1)))
        target.append(day[['peak_load']].values)
    
    output = np.array(output).reshape((-1))
    target = np.array(target).reshape((-1))
    
    return output, target


def rmse(output, target):
    return np.sqrt(((output - target) ** 2).mean())


if __name__ == '__main__':
    show_plot = False
    save = False
    
    if not os.path.isfile('data.csv'):
        prepare_data()
    
    data = pd.read_csv('data.csv', parse_dates=['date'], index_col='date', encoding='UTF-8', engine='python')
    train_data = data['2017-01-01':'2019-04-01']
    test_data = data['2019-04-02':'2019-04-08']
    
    workday_model, holiday_model = fit_model(train_data)
    
    output, target = predict(train_data)
    date = np.linspace(1, len(target), len(target))
    
    if show_plot:
        plt.plot(date, target)
        plt.plot(date, output)
    
    error = rmse(output, target)
    print('Training RMSE: {}'.format(error))
    
    output, target = predict(test_data)
    error = rmse(output, target)
    print('Test RMSE: {}'.format(error))
    
    if save:
        start_date = datetime.date(2019, 4, 2)
        date_list = [(start_date + datetime.timedelta(days=x)).strftime('%Y%m%d') for x in range(0, 7)]
        df_dict = {
            'date': date_list,
            'peak_load(MW)': np.around(output).astype(np.int)
        }
        
        df = pd.DataFrame(df_dict)
        df.to_csv('submission.csv', encoding='UTF-8', index=0)

if show_plot:
    plt.show()
