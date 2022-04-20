echo 'Inicializando DB'

/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "$(printenv SA_PASSWORD)"  -i init_db.sql
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "$(printenv SA_PASSWORD)"  -i init_tables.sql
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "$(printenv SA_PASSWORD)"  -i init_data.sql
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "$(printenv SA_PASSWORD)"  -i init_views.sql
