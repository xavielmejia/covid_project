from config.database_connection import Connect

connect = Connect('covid')
con = connect.connect_mssql_localhost()

print(con)
