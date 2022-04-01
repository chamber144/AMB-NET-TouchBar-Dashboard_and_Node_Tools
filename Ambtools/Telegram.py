

#sends a message to telegram
def send_message(msg):
    '''
    Send message via telegram bot
    :param msg:
    :return:
    '''

    # For payload params refer: https://core.telegram.org/bots/api#sendmessage
    payload = {
	'chat_id': Telegram_Chat_ID,
	'text': msg,
	'parse_mode': 'HTML'
    }
    return requests.post('https://api.telegram.org/bot{token}/sendMessage'.format(token=Telegram_Token),data=payload).content
