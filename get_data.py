import pandas as pd
import requests
import logging
from pytrends.request import TrendReq


class get_api():

    def __init__(self):
        self

    def get_api_countries(self):
        try:
            data = [requests.get(link, timeout=120).json() for link in self.values()]
            country_data = pd.DataFrame(data)
            country_data = country_data.transpose()
            country_data = country_data.set_index(0)
            country_data = country_data.reset_index(names='country')
            country_data.columns = self.keys()
            print(country_data)

            return country_data
        except Exception as e:
            logging.error(f'Problems with the data\n{e}')
            raise


class get_trends:

    def use_trends(kwords1:list, kwords2:list, country_list:list):

        try:
            pytrends = TrendReq(hl='es', tz=360)
            pytrends.build_payload(kw_list=kwords1, cat=0, timeframe='now 7-d',  geo='', gprop='')
            Data = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
            Words_1 = Data.filter(items=country_list, axis=0)

            pytrends.build_payload(kw_list=kwords2, cat=0, timeframe='now 7-d',  geo='', gprop='')
            Data = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
            Words_2 = Data.filter(items=country_list, axis=0)

            Data = pd.concat([Words_1, Words_2], axis=1)
            Data = Data.reset_index(names='country')
            return Data
        
        except Exception as e:
            logging.error(f'Problems with Pytrends\n{e}')
            raise



# data = [requests.get(i).json() for i in APIS.values()]
# country_data = pd.DataFrame(data)
# country_data = country_data.transpose()
# country_data = country_data.set_index(0)
# country_data = country_data.reset_index(names='country')
# country_data.columns = APIS.keys()
# print('Data countryAPI:_________________')
# print(country_data)
# country_list = list(country_data['country_names'])

# pytrends = TrendReq(hl='es', tz=360)

# pytrends.build_payload(kw_list=[
#     'swift',
#     'exchange',
#     'invertir',
#     'wallet',
#     'IBAN'
#     ], cat=0, timeframe='now 7-d',  geo='', gprop='')
# Data = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
# Words_1 = Data.filter(items=country_list, axis=0)


# pytrends.build_payload(kw_list=[
#     'neo banco',
#     'enviar dinero',
#     'remesa',
#     'compras en extranjero',
#     'divisas'
#     ], cat=0, timeframe='now 7-d',  geo='', gprop='')
# Data = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
# Words_2 = Data.filter(items=country_list, axis=0)

# Data = pd.concat([Words_1, Words_2], axis=1)
# Data = Data.reset_index(names='country')

# print('Data pytrends:_________________')
# print(Data)
