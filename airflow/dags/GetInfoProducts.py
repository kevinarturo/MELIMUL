import requests
import pymssql
import json
import pendulum
from airflow.decorators import dag, task



@dag(schedule_interval=None, start_date=pendulum.datetime(2022, 4, 20, tz="UTC"), catchup=False,tags=['MELI','Products'],)
def get_info_products():

    def get_connection():
        connection = pymssql.connect(server='192.168.1.92', user='sa', password='Pass!!1234!!#%', database='MELI_DB') 
        return connection

    @task()
    def clean_table():
        connection = get_connection()
        cursor = connection.cursor(as_dict=True)
        query = "TRUNCATE TABLE [MELI_DB].[dbo].[products]"
        cursor.execute(query)
        connection.commit()


    def obtener_sites_habilitados():
        connection = get_connection()
        cursor = connection.cursor(as_dict=True)
        query = """
            SELECT [id]
                ,[name]
                ,[default_currency_id]
                ,[enable]
            FROM [MELI_DB].[dbo].[sites] WHERE [enable] = 1
            """ 
        cursor.execute(query)

        result = [ row['id'] for row in cursor.fetchall()]
        return result

    def obtener_consultas_productos():
        connection = get_connection()
        cursor = connection.cursor(as_dict=True)
        query = """
            SELECT [id]
                ,[search]
                ,[enable]
            FROM [MELI_DB].[dbo].[searches] WHERE [enable] = 1
            """ 
        cursor.execute(query)

        result = [ row['search'] for row in cursor.fetchall()]
        return result

    @task()
    def extract():
        sites = obtener_sites_habilitados()
        busquedas = obtener_consultas_productos()

        current_token = requests.get('https://192.168.1.92:5500/token', verify=False).text
        complete_data = []

        for site in sites:
            for busqueda in busquedas:
                url = f"https://api.mercadolibre.com/sites/{site}/search?q={busqueda}"
                response = requests.request("GET", url, headers={'Authorization': f'Bearer {current_token}'})
                data = json.loads(response.text)["results"]
                for row in data:                                               #product name
                    clean_row  = (row['id'],row['seller']['id'],row['site_id'],row['title'] ,row['price'],row['condition'],row['thumbnail'],row['accepts_mercadopago'],row['category_id'], 1)
                    complete_data.append(clean_row)

        return complete_data



    @task()
    def load(complete_data):
        connection = get_connection() 
        cursor = connection.cursor(as_dict=True)
        query = """INSERT INTO [dbo].[products] VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""" 
        for row in complete_data:
            cursor.execute(query,tuple(row))
        connection.commit()
        

    clean_table()
    order_data = extract()
    load(order_data)

info_products = get_info_products()
