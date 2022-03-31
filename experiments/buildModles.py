from datetime import datetime
from pathlib import Path
import pickle
import warnings

import pandas as pd
from prophet import Prophet

warnings.simplefilter(action='ignore', category=FutureWarning)


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(['Vol.', 'Change %'], axis=1)
    columns_to_convert = list(df.columns)
    columns_to_convert.remove('Date')
    for column in columns_to_convert:
        df[column] = df[column].str.replace(',', '')
    df = df.astype({'Price': 'float', 'Open': 'float', 'High': 'float', 'Low': 'float'})
    return df


if __name__ == '__main__':
    models = {}
    for file in Path('datasets').glob('*HistoricalData.csv'):
        filename = file.name
        currency_name = filename.split('HistoricalData.csv')[0]

        raw_df = pd.read_csv(filepath_or_buffer=str(file),
                             parse_dates=['Date'],
                             date_parser=lambda dates: datetime.strptime(dates, '%b %d, %Y'),
                             dtype=str
                             )
        clean_df = clean_dataframe(raw_df)

        close_price_to_predict_on = clean_df[['Date', 'Price']]
        new_names = {
            "Date": "ds",
            "Price": "y",
        }
        close_price_to_predict_on = close_price_to_predict_on.rename(columns=new_names)
        model = Prophet(seasonality_mode="multiplicative", daily_seasonality=True)
        model.fit(close_price_to_predict_on)
        models[currency_name] = {'model': model}

    filename = f'models_{datetime.now().strftime("%d-%m-%Y")}.pickle'
    pickle.dump(models, open(filename, 'wb'))

    # TO DO: upload pickle file to SFTP server
