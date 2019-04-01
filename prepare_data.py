import os

import pandas as pd


def prepare_data():
    df = pd.read_csv('./data/holiday_date.csv', parse_dates=[0], encoding='UTF-8-sig', engine='python')
    df['holiday'] = pd.to_datetime(df['holiday']).dt.date
    holiday = df['holiday'].values
    
    df = pd.read_csv('./data/workday_date.csv', parse_dates=[0], encoding='UTF-8-sig', engine='python')
    df['workday'] = pd.to_datetime(df['workday']).dt.date
    workday = df['workday'].values
    
    df = pd.read_csv('./data/台灣電力公司_過去電力供需資訊.csv', parse_dates=['日期'], encoding='UTF-8-sig', engine='python')
    df.rename(columns={'尖峰負載(MW)': 'peak_load', '日期': 'date'}, inplace=True)
    data = df[['peak_load', 'date']]
    
    data['weekday'] = data['date'].dt.dayofweek
    data['workday'] = (~data['weekday'].isin([5, 6]) & ~data['date'].isin(holiday) | \
                       data['weekday'].isin([5, 6]) & data['date'].isin(workday)) * 1
    
    data = data.set_index('date')
    
    data['temperature'] = 0
    for filename in os.listdir('./data'):
        if filename.startswith('467490'):
            df = pd.read_csv(os.path.join('./data/', filename), encoding='UTF-8-sig', engine='python')
            date = pd.to_datetime(df['T Max Time']).dt.date
            head = date.head(1).values[0].strftime('%Y-%m-%d')
            tail = date.tail(1).values[0].strftime('%Y-%m-%d')
            data['temperature'][head:tail] = df['Temperature']
    
    df = pd.read_csv('./data/holiday_days.csv', index_col='date', encoding='UTF-8-sig', engine='python')
    data['holiday'] = df['holiday']
    
    data.to_csv('data.csv', encoding='UTF-8')
