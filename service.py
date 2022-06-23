from nameko.rpc import rpc
from dependencies.database import DatabaseProvider


class AccountService:
    name = 'account_service'
    database = DatabaseProvider()
    
    @rpc
    def account_registration(self, email_address, password):
        registration = self.database.account_registration(email_address, password)
        return registration
    
    
    @rpc
    def login_account(self, email_address, password):
        login = self.database.login_account(email_address, password)
        return login


class NewsService:
    name = 'news_service'
    database = DatabaseProvider()

    @rpc
    def add_news(self, arr_filename, text):
        add_news = self.database.add_news(arr_filename, text)
        return add_news
    
    
