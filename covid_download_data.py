# import pandas as pd
import requests 
import sys
from  config.database_connection import Connect
import time
import json
import os

start_program = time.time()
url_countries = r'https://api.covid19api.com/countries'

connect = Connect('COVID')
con_covid = connect.connect_mssql_localhost()



def extract_info(url):
    try:
        data = requests.get(url)
        data_json = data.json()
        return data_json
    except:
        err_type = str(sys.exc_info()[0])
        err_msg = str(sys.exc_info()[1])
        print(err_type, err_msg)
        return None


def insert_to_database(table_name, con, data_json):
    if con != None:
        cur = con.cursor()
        try:
            print('Inside insert function')
            start = time.time()
            print(table_name.lower()=='covidcountries')

            values = [tuple(dic.values()) for dic in data_json]

            if table_name.lower()=='covidcases':
                sql_del = ''' delete from {} '''.format(table_name)

                sql_insert = '''INSERT INTO {} (countryName, countryCode, province, city, cityCode, latitude, longitude, confirmed, deaths, recovered, active, date)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'''.format(table_name)

                sql_upd = ''' update {} set createdDate=getdate() '''.format(table_name)
            elif table_name.lower()=='covidcountries':
                sql_del = ''' delete from {} '''.format(table_name)

                sql_insert = '''INSERT INTO {} (name, slug, iso2) VALUES (?,?,?)'''.format(table_name)

                sql_upd = ''' update {} set createdDate=getdate() '''.format(table_name)
            else:
                print('Table specified does not exists')
                return

            if data_json:
                print('Start insert data')
                
                cur.execute(sql_del)
                print('Data has been deleted from {}'.format(table_name))
                
                cur.executemany(sql_insert, values)
                print('Data has been inserted to {}'.format(table_name))
                
                cur.execute(sql_upd)
                print('Field createdDate in table {} has been updated'.format(table_name))

                cur.commit()
                end = time.time()
                print('Time to insert data {}'.format(str(end - start)))

        except:
            err_type = str(sys.exc_info()[0])
            err_msg = str(sys.exc_info()[1])
            cur.rollback()
            print(err_type, err_msg)
        finally:
            cur.close()
    else:
        print('Connection is None')


# extract countries info from api
country_info = extract_info(url_countries)

# extract country name to a list
countries = [c['Country'] for c in country_info]

# insert countries data into mssql localhost
insert_to_database(table_name='covidCountries', con=con_covid, data_json=country_info)

data_list = []

# extract info for each country
print('reading data')
for country in countries:
    url = f'https://api.covid19api.com/total/dayone/country/{country}'
    data = extract_info(url)
    data_list.append(data)
print('Country data has been read it successfully!')

# save json as it was downloaded from the web
with open(os.path.join(os.getcwd(), r'docs\documents\data.txt'), 'w') as file:
    json.dump(data_list, file)

# insert data into COVID database in localhost mssql
insert_to_database(table_name='covidCases', con=con_covid, data_json=data)
end_program = time.time()
print('Program takes {} seconds'.format(end_program - start_program))