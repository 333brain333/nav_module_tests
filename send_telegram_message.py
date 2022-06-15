'''
Sends message with a existing telegram bot
'''
import requests
bot_token = ''
bot_chatID = ''
text = ''

class sendtext():
    '''
    Sends message to given chat id and using token
    '''
    def __init__(self, bot_token:str, bot_chatID:str):
        self.bot_token = bot_token
        self.bot_chatID = bot_chatID
    def send(self, bot_message:str):
        send_text = 'https://api.telegram.org/bot' +\
                self.bot_token + '/sendMessage?chat_id=' +\
                self.bot_chatID + '&parse_mode=Markdown&text='\
                + bot_message
        response = requests.get(send_text)
        return response.json()

if __name__=="__main__":
    send = sendtext('5263629888:AAGjFtC3ea2zqK13xluLx2bXzImi7aZRVN8','276541273')
    test = send.send('Test')
    print(test)
