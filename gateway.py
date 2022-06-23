import json
from unittest import result
from grpc import Status
from matplotlib.font_manager import json_dump
from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from requests import session
from dependencies.redis import SessionProvider
from werkzeug.wrappers import Response

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'data/news'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists('data'):
    os.mkdir('data')
if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
                app = Flask(__name__)
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
                
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
    
    
    @http('PUT', '/api/news')
    def edit_news(self, request):
        return None
    
    
    @http('DELETE', '/api/news')
    def delete_news(self, request):
        return None



    
    
        