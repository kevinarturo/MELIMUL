
@echo off

if not exist "./airflow/dags"  mkdir "./airflow/dags" 
if not exist "./airflow/logs"  mkdir "./airflow/logs" 
if not exist "./airflow/plugins" mkdir "./airflow/plugins"

:: Bajar servicios si estan activos
docker-compose -f compose-airflow.yml down
docker-compose -f compose-meli.yml down

:: Inicializacion del entorno 
echo "Inicializando airflow..."
docker-compose -f compose-airflow.yml up airflow-init

:: Levantar los servicios de airflow en background
echo "Levantando servicios de airflow"
docker-compose -f compose-airflow.yml up -d

:: Levantar la arquitectura del proyecto de MELI

echo "Creando e inicializando proyecto"
docker-compose -f compose-meli.yml build --no-cache

echo "Montando proyecto..."
docker-compose -f compose-meli.yml up -d

echo "Proyecto Montado Airflow: http://localhost:8080 SQLServer: localhost:1433"
