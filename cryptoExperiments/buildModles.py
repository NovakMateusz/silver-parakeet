from datetime import datetime
from typing import Optional
import os
from pathlib import Path
import pickle
from uuid import uuid4
import warnings
import sys

from dropbox import Dropbox
from dropbox.exceptions import AuthError
import pandas as pd
from prophet import Prophet

warnings.simplefilter(action='ignore', category=FutureWarning)


def connect_to_dropbox(api_key: str) -> Optional[Dropbox]:
    dbx = None
    try:
        dbx = Dropbox(api_key)
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx


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

    model_hash = str(uuid4())
    filename = f'{model_hash}.pickle'

    pickle_object = pickle.dumps(models)

    dropbox_key = os.environ.get("DROPBOX_API_KEY")
    dropbox_connection = connect_to_dropbox(dropbox_key)
    dropbox_path = f'/forecastingModels/{filename}'
    print(f'Object size: {sys.getsizeof(pickle_object)}')

    dropbox_connection.files_upload(pickle_object, dropbox_path)

    print(f'Model hash: {model_hash}')
    print(f'Has been saved {dropbox_path}')
