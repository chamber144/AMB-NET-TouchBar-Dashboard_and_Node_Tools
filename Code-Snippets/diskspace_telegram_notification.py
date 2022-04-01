#Enter your Settings here:
#------------------------------------------------------------

#enter your Telegram Token like this '1366402345:AA41ZAEV...' and chat id '514579...'
Telegram_Token = ''
Telegram_Chat_ID = ''


#Enter this Nodes address
Nodeaddress = ''


#Specify your node type ('Atlas', 'Apollo' or 'Hermes')
Nodetype = 'Atlas'


#To be consistent with the main telegram script, please define the number of this Node.
Nodenumber = '1'


#At which disk-treshold (gigabyte) do you want the warning to trigger?
freeSpaceTreshold = '4'


#---------------------------------------------------------------

import requests
import shutil

lowSpace = '\u26A0\uFE0F'

#send to telegram function
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

total, used, free = shutil.disk_usage("/")

print('Total: %d GiB' % (total // (2**30)))
print('Used: %d GiB' % (used // (2**30)))
free =('%d' % (free // (2**30)))
print(float(free))

if Nodetype.lower() in ['atlas','apollo','hermes']:
    Nodename = (Nodetype+' Node '+Nodenumber)
    if float(free) <= float(freeSpaceTreshold):
        send_message(lowSpace+' Your '+Nodename+' is running low on free disk space with '+free+' gigabytes remaining.\nPlease upgrade this Nodes SSD:\n<a href=\"https://explorer.ambrosus.com/apollo/'+Nodeaddress+'\">'+Nodeaddress+'</a>\n\n-------------------------------')
elif Nodetype.lower() in ['none', '', None]:
    if float(free) <= float(freeSpaceTreshold):
        send_message(lowSpace+' Your Server without Node is running low on free disk space with '+free+' gigabytes remaining.\n\n-------------------------------')
else:
    send_message('You specified an unknown Node type (\''+Nodetype+'\') for your Node with Address \n<a href=\"https://explorer.ambrosus.com/apollo/'+Nodeaddress+'\">'+Nodeaddress+'</a>. \nPlease update the notification script with a valid node type\n\n-------------------------------')
