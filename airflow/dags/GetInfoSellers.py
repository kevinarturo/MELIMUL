import requests
import pymssql
import json
import pendulum
from airflow.decorators import dag, task



@dag(schedule_interval=None, start_date=pendulum.datetime(2022, 4, 20, tz="UTC"), catchup=False,tags=['MELI','Products'],)
def get_info_sellers():

    def get_connection():
        connection = pymssql.connect(server='192.168.1.92', user='sa', password='Pass!!1234!!#%', database='MELI_DB') 
        return connection

    @task()
    def clean_table():
        connection = get_connection()
        cursor = connection.cursor(as_dict=True)
        query = "TRUNCATE TABLE [MELI_DB].[dbo].[sellers]"
        cursor.execute(query)
        connection.commit()


    def obtener_sellers_ids():
        connection = get_connection()
        cursor = connection.cursor(as_dict=True)
        query = "SELECT DISTINCT [seller_id] FROM [MELI_DB].[dbo].[products] " 
        cursor.execute(query)

        result = [ row['seller_id'] for row in cursor.fetchall()]
        return result
    
    def complete_address(obj_address):
        address = ''
        if type(obj_address) == dict:
            for key in obj_address.keys():
                address = address + key + ' ' + obj_address[key] + '; '
        if type(obj_address) == str:
            address = obj_address
        return address


    @task()
    def extract():
        sellers = obtener_sellers_ids()

        current_token = requests.get('https://192.168.1.92:5500/token', verify=False).text
        complete_data = []

        for seller in sellers:
            url = f"https://api.mercadolibre.com/users/{seller}"
            response = requests.request("GET", url, headers={'Authorization': f'Bearer {current_token}'})
            row = json.loads(response.text)                                             
            clean_row  = (row['id'],row['nickname'],complete_address(row['address']))
            complete_data.append(clean_row)

        return complete_data



    @task()
    def load(complete_data):
        connection = get_connection() 
        cursor = connection.cursor(as_dict=True)
        query = """INSERT INTO [dbo].[sellers] VALUES (%s, %s, %s)""" 
        for row in complete_data:
            cursor.execute(query,tuple(row))
        connection.commit()
        

    clean_table()
    order_data = extract()
    load(order_data)

info_sellers = get_info_sellers()

