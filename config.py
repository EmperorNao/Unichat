class Config:

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


# init config for db
def init_config():

    print('Файловый ввод, а не консольный: (Y/N)')
    t = input().lower()
    if t == 'y':
        s = open('configs/db_config.txt', "r", encoding="UTF-8").read()
        t = []
        for line in s.split('\n'):
            t.append(line)
        host, user, password = t[0], t[1], t[2]
    else:
        print('Введите хост:')
        host = input()
        print('Введите пользователя:')
        user = input()
        print('Введите пароль:')
        password = input()
    return Config(host, user, password, 'unichat')
