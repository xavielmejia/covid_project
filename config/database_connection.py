import pyodbc
# from sqlalchemy.engine import URL
import os
import logging
import sys

# logging configuration
FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()

class Connect():
    '''
    class to handle connections to COVID project
    '''

    def __init__(self, database):
        self.database = database


    def connect_mssql_localhost(self):
        '''
        Method to connect to connect to Microsoft SQL Localhost using the database specified
        '''
        try:
            connection_string = os.environ.get('COVID_MSSQL') # get connection string from environment variables
            # connection_url = URL.create('mssql+pyodbc', query={'odbc_connect': connection_string})
            
            con =  pyodbc.connect(connection_string) # set the conection with pyodbc
            if con != None:
                logger.debug('Connection succesfully established!')
                return con
            else:
                logger.debug('Connection could not be established to the database')
        except:
            err_type = str(sys.exc_info()[0]) # get the error type if occurs
            err_msg = str(sys.exc_info()[1]) # get the error message if occurs
            logger.debug('Something went wrong while trying to connect to {0} database, error type: {1}, error message: {2}'.format(self.database, err_type, err_msg)) 

# print(Connect('covid').connect_mssql_localhost())
