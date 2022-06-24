# from unittest import result
# from urllib import response
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
        
        cursor.close()
        return {
            'response_code': 200,
            'response_data': {
                "status": "success",
                "message": "Add news successful"
            }
        }
    
    
    def checking_news_availability(self, news_id):
        cursor = self.connection.cursor(dictionary=True)
        response = None
        
        sql = 'SELECT COUNT(*) AS x, news.* FROM `news` WHERE id = %s AND deleted = 0'
        cursor.execute(sql, [int(news_id)])
        result = cursor.fetchone()
        
        if result['x'] > 0:
            response = {
                'response_code': 200,
                'response_data': {
                    "status": "success",
                    "message": "News found",
                    "data": {
                        'id': result['id'],
                        'text': result['text'],
                        'deleted': result['deleted'],
                        'created_on': result['created_on']
                    }
                }
            }          
        else:
            response = {
                'response_code': 404,
                'response_data': {
                    "status": "error",
                    "message": "News not found"
                }
            }
        
        cursor.close()
        return response
    
    
    def edit_news_text(self, news_id, text):
        cursor = self.connection.cursor(dictionary=True)
        
        sql = 'UPDATE `news` SET `text`=%s WHERE id = %s'
        cursor.execute(sql, [str(text), int(news_id)])
        self.connection.commit()
        
        cursor.close()
        return {
            'response_code': 200,
            'response_data': {
                "status": "success",
                "message": "Edit news text successful"
            }
        }
    
    
    def add_news_file(self, news_id, arr_filename):
        cursor = self.connection.cursor(dictionary=True)
        
        for i in range(len(arr_filename)):
            sql = 'INSERT INTO `news_files`(`id`, `filename`, `deleted`, `id_news`) VALUES (NULL, %s, %s, %s)'
            cursor.execute(sql, [str(arr_filename[i]), int(0), int(news_id)])
        
        self.connection.commit()
        cursor.close()
        return {
            'response_code': 200,
            'response_data': {
                "status": "success",
                "message": "Add news file successful"
            }
        }
    
    
    def delete_news(self, news_id):
        cursor = self.connection.cursor(dictionary=True)
        
        sql = 'UPDATE `news_files` SET `deleted`=%s WHERE id_news = %s'
        cursor.execute(sql, [int(1), int(news_id)])
        
        sql = 'UPDATE `news` SET `deleted`=%s WHERE id = %s'
        cursor.execute(sql, [int(1), int(news_id)])
        
        self.connection.commit()
        cursor.close()
        return {
            'response_code': 200,
            'response_data': {
                "status": "success",
                "message": "Delete news successful"
            }
        }
    
    
    def delete_news_file(self, news_id, file_id):
        cursor = self.connection.cursor(dictionary=True)
        
        sql = 'SELECT COUNT(*) AS x FROM `news_files` WHERE id_news = %s AND id = %s'
        cursor.execute(sql, [int(news_id), int(file_id)])
        result = cursor.fetchone()
        
        if result['x'] <= 0:
            return {
                'response_code': 404,
                'response_data': {
                    "status": "error",
                    "message": "File not found"
                }
            }
        
        sql = 'UPDATE `news_files` SET `deleted`=%s WHERE id = %s AND id_news = %s'
        cursor.execute(sql, [int(1), int(file_id), int(news_id)])
        
        self.connection.commit()
        cursor.close()
        return {
            'response_code': 200,
            'response_data': {
                "status": "success",
                "message": "Delete news file successful"
            }
        }
    
    
    def get_all_news(self):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        
        sql = 'SELECT * FROM `news` WHERE deleted = %s'
        cursor.execute(sql, [int(0)])
        
        for row in cursor.fetchall():
            files = []
            
            sql_get_news_files = 'SELECT * FROM `news_files` WHERE id_news = %s AND deleted = %s'
            cursor.execute(sql_get_news_files, [int(row['id']), int(0)])
            
            for file in cursor.fetchall():
                files.append({
                    'id': file['id'],
                    'filename': file['filename']
                })
            
            result.append({
                'id': row['id'],
                'text': row['text'],
                'created_on': row['created_on'],
                'files': files
            })
        
        cursor.close()
        return {
            'response_code': 200,
            'response_data': {
                "status": "success",
                "data": result
            }
        }
    
    
    def get_news_by_id(self, news_id):
        cursor = self.connection.cursor(dictionary=True)
        response = None
        files = []
        
        sql = 'SELECT * FROM `news` WHERE deleted = %s AND id = %s'
        cursor.execute(sql, [int(0), int(news_id)])
        result = cursor.fetchone()
        
        sql_get_news_files = 'SELECT * FROM `news_files` WHERE id_news = %s AND deleted = %s'
        cursor.execute(sql_get_news_files, [int(result['id']), int(0)])
        
        for file in cursor.fetchall():
            files.append({
                'id': file['id'],
                'filename': file['filename']
            })
        
        response = {
            'id': result['id'],
            'text': result['text'],
            'created_on': result['created_on'],
            'files': files
        }
        
        cursor.close()
        return {
            'response_code': 200,
            'response_data': {
                "status": "success",
                "data": response
            }
        }
    
    
    def get_file(self, file_id):
        cursor = self.connection.cursor(dictionary=True)
        response = None
        
        sql = 'SELECT COUNT(*) AS x, news_files.* FROM `news_files` WHERE id = %s AND deleted = 0'
        cursor.execute(sql, [int(file_id)])
        result = cursor.fetchone()
        
        if result['x'] <= 0:
            response = {
                'response_code': 404,
                'response_data': {
                    "status": "error",
                    "message": "File not found"
                }
            }
        else:
            response = {
                'response_code': 200,
                'response_data': {
                    "status": "success",
                    "data": {
                        'id': result['id'],
                        'filename': result['filename']
                    }
                }
            }
        
        cursor.close()
        return response


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
