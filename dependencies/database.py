from urllib import response
from nameko.extensions import DependencyProvider
import mysql.connector
from mysql.connector import Error
import mysql.connector.pooling


class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection


    def account_registration(self, email_address, password):
        cursor = self.connection.cursor(dictionary=True)
        response = None
        
        sql = 'SELECT COUNT(*) AS x FROM `account` WHERE email_address = %s'
        cursor.execute(sql, [str(email_address)])
        result = cursor.fetchone()
        
        if result['x'] > 0:
            response = {
                'response_code': 400,
                'response_data': {
                    "status": "error",
                    "message": "Email already taken"
                }
            }
        else:
            sql = 'INSERT INTO `account`(`id`, `email_address`, `password`) VALUES (NULL, %s, md5(%s))'
            cursor.execute(sql, [str(email_address), str(password)])
            self.connection.commit()
            
            response = {
                'response_code': 201,
                'response_data': {
                    "status": "success",
                    "message": "Account created successfully"
                }
            }
        
        cursor.close()
        return response
    
    
    def login_account(self, email_address, password):
        cursor = self.connection.cursor(dictionary=True)
        response = None
        
        sql = 'SELECT COUNT(*) AS x FROM `account` WHERE email_address = %s AND password = md5(%s)'
        cursor.execute(sql, [str(email_address), str(password)])
        result = cursor.fetchone()
        
        if result['x'] > 0:
            response = {
                'response_code': 200,
                'response_data': {
                    "status": "success",
                    "message": "Logged in successfully"
                }
            }
        else:
            response = {
                'response_code': 401,
                'response_data': {
                    "status": "error",
                    "message": "Unauthorized: invalid credentials (wrong email/password)"
                }
            }
        
        cursor.close()
        return response
    
    
    def add_news(self, arr_filename, text):
        cursor = self.connection.cursor(dictionary=True)
        
        sql = 'INSERT INTO `news`(`id`, `text`, `deleted`, `created_on`) VALUES (NULL, %s, %s, CURRENT_TIMESTAMP)'
        cursor.execute(sql, [str(text), int(0)])
        self.connection.commit()
        lastRowId = cursor.lastrowid
        
        for i in range(len(arr_filename)):
            sql = 'INSERT INTO `news_files`(`id`, `filename`, `deleted`, `id_news`) VALUES (NULL, %s, %s, %s)'
            cursor.execute(sql, [str(arr_filename[i]), int(0), int(lastRowId)])
            self.connection.commit()
        
        return {
            'response_code': 200,
            'response_data': {
                "status": "success",
                "message": "Added news successfully"
            }
        }
        
        
        
        
       
        
        


class DatabaseProvider(DependencyProvider):

    connection_pool = None

    def setup(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=32,
                pool_reset_session=True,
                host='127.0.0.1',
                database='department_news_board',
                user='root',
                password=''
            )
        except Error as e:
            print("Error while connecting to MySQL using Connection pool ", e)
    
    
    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())
