FROM mcr.microsoft.com/mssql/server:2017-latest

ENV ACCEPT_EULA=Y
ENV SA_PASSWORD=Pass!!1234!!#%
USER root

WORKDIR /src

# Copiar el archivo de configuracion inicial de la DB
COPY init_db.sql ./
COPY init_tables.sql ./
COPY init_data.sql ./
COPY init_views.sql ./
COPY setup.sh ./

# Se asignan permisos de ejeecución al script de setup
RUN chmod +x ./setup.sh

RUN (/opt/mssql/bin/sqlservr &) | grep -q "Service Broker manager has started" && ./setup.sh && pkill sqlservr