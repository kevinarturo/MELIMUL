echo "Creando e inicializando proyecto"
docker-compose -f compose-meli.yml build --no-cache

echo "Montando proyecto..."
docker-compose -f compose-meli.yml up -d