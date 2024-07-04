import os
import logging
from get_data import get_api
from data_lead import lead
from dotenv import load_dotenv

load_dotenv()

APIS = {
    'country_names': 'https://country.io/names.json',
    'capitals_names': 'https://country.io/capital.json',
    'continents': 'https://country.io/continent.json',
    'ISO_codes': 'https://country.io/iso3.json',
    'phone_codes': 'https://country.io/phone.json',
    'currency_codes': 'https://country.io/currency.json',
}

logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s ::MainModule-> %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

def main():
    user_credentials = {
    "REDSHIFT_USERNAME" : os.getenv('REDSHIFT_USERNAME'),
    "REDSHIFT_PASSWORD" : os.getenv('REDSHIFT_PASSWORD'),
    "REDSHIFT_HOST" : os.getenv('REDSHIFT_HOST'),
    "REDSHIFT_PORT" : os.getenv('REDSHIFT_PORT', '5439'),
    "REDSHIFT_DBNAME" : os.getenv('REDSHIFT_DBNAME')
    }

    schema = 'moisesmarquinaj_coderhouse'
    data_conn = lead(user_credentials, schema)

    try:
        data = get_api.get_api_countries(APIS)
        data_conn.create_table(data=data, table_name='api_countries')
        logging.info(f"Data uploaded to -> {schema}")

    except Exception as e:
        logging.error(f"Not able to upload data\n{e}")


if __name__ == "__main__":
    main()
