
class Config():

    def __init__(self, host='localhost', user='root', password='password', db_name=None):
        self.host = host
        self.user = user
        self.password = password
        self.db = db_name

    def get_settings(self):
        return dict(host=self.host,
                    user=self.user,
                    password=self.password,
                    db=self.db)

