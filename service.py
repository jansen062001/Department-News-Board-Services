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
    
    
    @rpc
    def checking_news_availability(self, news_id):
        news_availability = self.database.checking_news_availability(news_id)
        return news_availability
    
    
    @rpc
    def edit_news_text(self, news_id, text):
        edit_news_text = self.database.edit_news_text(news_id, text)
        return edit_news_text
    
    
    @rpc
    def add_news_file(self, news_id, arr_filename):
        add_news_file = self.database.add_news_file(news_id, arr_filename)
        return add_news_file
    
    
    @rpc
    def delete_news(self, news_id):
        delete_news = self.database.delete_news(news_id)
        return delete_news
    
    
    @rpc
    def delete_news_file(self, news_id, file_id):
        delete_news_file = self.database.delete_news_file(news_id, file_id)
        return delete_news_file
    
    
    @rpc
    def get_all_news(self):
        get_all_news = self.database.get_all_news()
        return get_all_news
    
    
    @rpc
    def get_news_by_id(self, news_id):
        get_news_by_id = self.database.get_news_by_id(news_id)
        return get_news_by_id
    
    
    @rpc
    def get_file(self, file_id):
        file = self.database.get_file(file_id)
        return file
