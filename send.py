import requests
from bot_token import TOKEN


class Enviar:

    def __init__(self):
        self.token = TOKEN
        self.weeks = 8

    def imagen(self, dato, comuna, user_id):
        files = {'photo':open(f"images/{dato}-{comuna}-weeks{self.weeks}.png",'rb')}
        resp = requests.post(f"https://api.telegram.org/bot{self.token}/sendPhoto?chat_id={user_id}",files=files)
        print(resp)

    def texto(self, user_id, text):
        resp = requests.post(f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={user_id}&text={text}")
        print(resp)
