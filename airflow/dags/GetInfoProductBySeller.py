import requests
import pymssql
import json
import pendulum
from airflow.decorators import dag, task



@dag(schedule_interval=None, start_date=pendulum.datetime(2022, 4, 20, tz="UTC"), catchup=False,tags=['MELI','Products'],)
def get_info_products_by_seller():

    def get_connection():
        connection = pymssql.connect(server='192.168.1.92', user='sa', password='Pass!!1234!!#%', database='MELI_DB') 
        return connection

    @task()
    def clean_table():
        connection = get_connection()
        cursor = connection.cursor(as_dict=True)
        query = "DELETE FROM [MELI_DB].[dbo].[products] WHERE [is_from_search] = 0"
        cursor.execute(query)
        connection.commit()


    def obtener_sellers_data():
        connection = get_connection()
        cursor = connection.cursor(as_dict=True)
        query = """
            SELECT DISTINCT 
                T1.[id]
                ,T2.site_id
            FROM [MELI_DB].[dbo].[sellers] AS T1
            INNER JOIN [MELI_DB].[dbo].[products] AS T2
            ON T1.id = T2.seller_id
            """ 
        cursor.execute(query)

        result = [ {'id':row['id'], 'site': row['site_id'] } for row in cursor.fetchall()]
        return result

    @task()
    def extract():
        sellers = obtener_sellers_data()
       
        current_token = requests.get('https://192.168.1.92:5500/token', verify=False).text
        complete_data = []

        for seller in sellers:
            seller_id = seller['id']
            site_id = seller['site']

            url = f"https://api.mercadolibre.com/sites/{site_id}/search?seller_id={seller_id}"
            response = requests.request("GET", url, headers={'Authorization': f'Bearer {current_token}'})
            data = json.loads(response.text)["results"]
            for row in data:                                               #product name
                clean_row  = (row['id'],row['seller']['id'],row['site_id'],row['title'] ,row['price'],row['condition'],row['thumbnail'],row['accepts_mercadopago'],row['category_id'], 0)
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

info_products = get_info_products_by_seller()
