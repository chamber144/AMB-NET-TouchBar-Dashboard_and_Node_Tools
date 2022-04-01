import yaml

def read_yaml(file_path):
	try:
		with open(file_path, "r") as f:
			return yaml.safe_load(f)
	except FileNotFoundError as e:
		print('file not found')
	except yaml.scanner.ScannerError as e:
		print('ScannerError raised')
	except yaml.scanner.ParserError as e:
		print('ParserError raised')

conf = read_yaml("ambtools-settings.yaml")

Telegram_Token = conf['Telegram_Token']
Telegram_Chat_ID = conf['Telegram_Chat_ID']
atlasnodes = conf['atlasnodes']
apollonodes = conf['apollonodes']
Nodetype = conf['Nodetype']
Nodenumber = conf['Nodenumber']
REBOOT_ON_ZOMBIES = conf['rebootOnZombies']

#Enter this Nodes address
if Nodetype == 0:
	Nodeaddress = atlasnodes[Nodenumber-1]
elif Nodetype == 1:
	Nodeaddress = apollonodes[Nodenumber-1]
else:
	Nodeaddress = 'N/A'

#how about using psutil?
import subprocess
import re
import os
from datetime import datetime

rebootOnZombies = True
zombie_emoji = '\U0001f9df'
scream_emoji = '\U0001f631'
logFile = 'zombies.log'


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

#gives back a list of all zombie processes with [status, PID, PPID, name]
def get_Zombies():
	child = subprocess.Popen(['ps','-A','-ostat,pid,ppid,fname'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	myZombies = []
	for line in child.stdout:
		columns = " ".join(re.split("\s+", line.decode(), flags=re.UNICODE)).split(' ')
		if 'Z' in columns[0].upper():
			myZombies.append(columns)

	return myZombies

def logEvent(msg):
	print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + ': ' + msg, file=open(logFile, 'a'))


zombies = get_Zombies()
if len(zombies) > 0:
	logMessage = 'Amb-Tools: '+str(len(zombies))+' Zombie(s) found: '
	for zomb in zombies:
		logMessage += zomb[3]+'('+zomb[1]+'), '
	logMessage = logMessage[:-1]            #removing last comma of string

	logEvent(logMessage)

	if rebootOnZombies:
		logEvent('reboot system...')
		send_message(logMessage + '\n' + zombie_emoji+' reboot due to zombie invasion '+zombie_emoji)

		err = os.system('reboot')
		if err != 0:
			logEvent('error: reboot failed! (no permission?)')
			send_message('Reboot failed probably due to missing sudo/root permission... Zombies still alive '+scream_emoji+zombie_emoji+zombie_emoji)
	else:
		logEvent('no action performed')
		send_message(zombie_emoji + logMessage + '\nrebootOnZombies == False, no action performed!')
else:
	print('no Zombies found...')
