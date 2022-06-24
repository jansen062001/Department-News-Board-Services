# from fileinput import filename
import json
# from unittest import result
# from grpc import Status
# from matplotlib.font_manager import json_dump
from nameko.rpc import RpcProxy
from nameko.web.handlers import http
# from requests import session
from dependencies.redis import SessionProvider
from werkzeug.wrappers import Response
import os
# from flask import Flask, flash, request, redirect, url_for, send_from_directory, current_app
from flask import Flask, send_from_directory
from werkzeug.utils import secure_filename
import datetime


UPLOAD_FOLDER = 'data/news'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
EXTENSION_HEADER = {
    'txt': 'text/plain',
    'pdf': 'application/pdf',
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'gif': 'image/gif'
}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists('data'):
    os.mkdir('data')
if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


class NewsBoardGatewayService:
    name = 'news_board_gateway'
    account_rpc = RpcProxy('account_service')
    news_board_rpc = RpcProxy('news_service')
    session_provider = SessionProvider()
    
    @http('POST', '/api/account')
    def account_registration(self, request):
        data = request.json
        
        registration = self.account_rpc.account_registration(data['email_address'], data['password'])
        
        return int(registration['response_code']), json.dumps(registration['response_data'])
    
    
    @http('POST', '/api/account/login')
    def login_account(self, request):
        data = request.json
        
        login = self.account_rpc.login_account(data['email_address'], data['password'])
        
        if int(login['response_code']) != 200:
            return int(login['response_code']), json.dumps(login['response_data'])
        
        cookies = request.cookies.get('SESSID')
        user_data = {
            'email_address': data['email_address']
        }
        
        if cookies == None:
            session_id = self.session_provider.set_session(user_data)
            response = Response(json.dumps(login['response_data']))
            response.set_cookie('SESSID', session_id)
            
            return response
        else:
            session_data = self.session_provider.get_session(cookies)
            
            if session_data['email_address'] == data['email_address']:
                return json.dumps(login['response_data'])
            else:
                session_id = self.session_provider.set_session(user_data)
                response = Response(json.dumps(login['response_data']))
                response.set_cookie('SESSID', session_id)
                
                return response
    
    
    @http('GET', '/api/account/logout')
    def logout_account(self, request):
        logout = self.session_provider.delete_session()
        response = Response(json.dumps({
            "status": "success",
            "message": "Logged out successfully"
        }))

        if logout:
            response.delete_cookie('SESSID')
        
        return response
    
    
    @http('POST', '/api/news')
    def add_news(self, request):
        cookies = request.cookies.get('SESSID')
        if cookies == None:
            return 401, json.dumps({
                "status": "error",
                "message": "Login required"
            })
         
        if 'file' not in request.files:
            return 400, json.dumps({
                "status": "error",
                "message": "No file part"
            })
        
        files = request.files.getlist('file')
        for file in files:
            if file.filename == '':
                return 400, json.dumps({
                    "status": "error",
                    "message": "No selected file"
                })
        
        arrFilename = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                arrFilename.append(filename)
            else:
                return 415, json.dumps({
                    "status": "error",
                    "message": "Unsupported Media Type"
                })
        
        add_news = self.news_board_rpc.add_news(arrFilename, request.form['text'])
        
        return int(add_news['response_code']), json.dumps(add_news['response_data'])
    
    
    @http('PUT', '/api/news/<int:news_id>')
    def edit_news_text(self, request, news_id):
        cookies = request.cookies.get('SESSID')
        if cookies == None:
            return 401, json.dumps({
                "status": "error",
                "message": "Login required"
            })
        
        news_availability = self.news_board_rpc.checking_news_availability(news_id)
        if int(news_availability['response_code']) != 200:
            return int(news_availability['response_code']), json.dumps(news_availability['response_data'])
        
        timestamp = news_availability['response_data']['data']['created_on']
        date = datetime.datetime.strptime(timestamp.split('T')[0], '%Y-%m-%d')
        current_date = datetime.datetime.date(datetime.datetime.now())
        
        if current_date >= datetime.datetime.date(date + datetime.timedelta(days=30)):
            return 404, json.dumps({
                "status": "error",
                "message": "News has been archived"
            })
        
        data = request.json
        
        edit_news_text = self.news_board_rpc.edit_news_text(news_id, data['text'])
        
        return int(edit_news_text['response_code']), json.dumps(edit_news_text['response_data'])
    
    
    @http('POST', '/api/news/<int:news_id>/file')
    def add_news_file(self, request, news_id):
        cookies = request.cookies.get('SESSID')
        if cookies == None:
            return 401, json.dumps({
                "status": "error",
                "message": "Login required"
            })
        
        news_availability = self.news_board_rpc.checking_news_availability(news_id)
        if int(news_availability['response_code']) != 200:
            return int(news_availability['response_code']), json.dumps(news_availability['response_data'])
        
        timestamp = news_availability['response_data']['data']['created_on']
        date = datetime.datetime.strptime(timestamp.split('T')[0], '%Y-%m-%d')
        current_date = datetime.datetime.date(datetime.datetime.now())
        
        if current_date >= datetime.datetime.date(date + datetime.timedelta(days=30)):
            return 404, json.dumps({
                "status": "error",
                "message": "News has been archived"
            })
        
        if 'file' not in request.files:
            return 400, json.dumps({
                "status": "error",
                "message": "No file part"
            })
        
        files = request.files.getlist('file')
        for file in files:
            if file.filename == '':
                return 400, json.dumps({
                    "status": "error",
                    "message": "No selected file"
                })
        
        arrFilename = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                arrFilename.append(filename)
            else:
                return 415, json.dumps({
                    "status": "error",
                    "message": "Unsupported Media Type"
                })
        
        add_news_file = self.news_board_rpc.add_news_file(news_id, arrFilename)
        
        return int(add_news_file['response_code']), json.dumps(add_news_file['response_data'])
    
    
    @http('DELETE', '/api/news/<int:news_id>')
    def delete_news(self, request, news_id):
        cookies = request.cookies.get('SESSID')
        if cookies == None:
            return 401, json.dumps({
                "status": "error",
                "message": "Login required"
            })
        
        news_availability = self.news_board_rpc.checking_news_availability(news_id)
        if int(news_availability['response_code']) != 200:
            return int(news_availability['response_code']), json.dumps(news_availability['response_data'])
        
        delete_news = self.news_board_rpc.delete_news(news_id)
        
        return int(delete_news['response_code']), json.dumps(delete_news['response_data'])
    
    
    @http('DELETE', '/api/news/<int:news_id>/file/<int:file_id>')
    def delete_news_file(self, request, news_id, file_id):
        cookies = request.cookies.get('SESSID')
        if cookies == None:
            return 401, json.dumps({
                "status": "error",
                "message": "Login required"
            })
        
        news_availability = self.news_board_rpc.checking_news_availability(news_id)
        if int(news_availability['response_code']) != 200:
            return int(news_availability['response_code']), json.dumps(news_availability['response_data'])
        
        timestamp = news_availability['response_data']['data']['created_on']
        date = datetime.datetime.strptime(timestamp.split('T')[0], '%Y-%m-%d')
        current_date = datetime.datetime.date(datetime.datetime.now())
        
        if current_date >= datetime.datetime.date(date + datetime.timedelta(days=30)):
            return 404, json.dumps({
                "status": "error",
                "message": "News has been archived"
            })
        
        delete_news_file = self.news_board_rpc.delete_news_file(news_id, file_id)
        
        return int(delete_news_file['response_code']), json.dumps(delete_news_file['response_data'])
    
    
    @http('GET', '/api/news')
    def get_all_news(self, request):
        get_all_news = self.news_board_rpc.get_all_news()
        
        return int(get_all_news['response_code']), json.dumps(get_all_news['response_data'])
    
    
    @http('GET', '/api/news/<int:news_id>')
    def get_news_by_id(self, request, news_id):
        news_availability = self.news_board_rpc.checking_news_availability(news_id)
        if int(news_availability['response_code']) != 200:
            return int(news_availability['response_code']), json.dumps(news_availability['response_data'])
        
        get_news_by_id = self.news_board_rpc.get_news_by_id(news_id)
        
        return int(get_news_by_id['response_code']), json.dumps(get_news_by_id['response_data'])
    
    
    @http('GET', '/api/news/file/<int:file_id>')
    def download_file(self, request, file_id):
        file = self.news_board_rpc.get_file(file_id)
        
        if int(file['response_code']) != 200:
            return int(file['response_code']), json.dumps(file['response_data'])
        
        filename = file['response_data']['data']['filename']
        response = Response(open(UPLOAD_FOLDER + '/' + filename, 'rb').read())
        file_type = filename.split('.')[-1]
        
        response.headers['Content-Type'] = EXTENSION_HEADER[file_type]
        response.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        
        return response
