import Ambtools_library as atl
import Emoji
import Telegram
# CUT: read_yaml()

conf = atl.read_yaml("ambtools-settings.yaml")

Telegram_Token = conf['Telegram_Token']
Telegram_Chat_ID = conf['Telegram_Chat_ID']
atlasnodes = conf['atlasnodes']
apollonodes = conf['apollonodes']
Nodetype = conf['Nodetype']
Nodenumber = conf['Nodenumber']
REBOOT_ON_ZOMBIES = conf['rebootOnZombies']

#Enter this Nodes address
if Nodetype.lower() == 'atlas':
	Nodeaddress = atlasnodes[Nodenumber-1]
elif Nodetype.lower() == 'apollo':
	Nodeaddress = apollonodes[Nodenumber-1]
else:
	Nodeaddress = 'N/A'

#how about using psutil?
import subprocess
import re
import os
from datetime import datetime

zombie_emoji = Emoji.zombie #'\U0001f9df'
scream_emoji = Emoji.scream #'\U0001f631'
logFile = 'zombies.log'



#gives back a list of all zombie processes with [status, PID, PPID, name]
def get_Zombies():
	child = subprocess.Popen(['ps','-A','-ostat,pid,ppid,fname'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	myZombies = []
	for line in child.stdout:
		columns = " ".join(re.split("\s+", line.decode(), flags=re.UNICODE)).split(' ')
		if 'Z' in columns[0].upper():
			myZombies.append(columns)

	return myZombies

def logEvent(msg, logFile):
	print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + ': ' + msg, file=open(logFile, 'a'))


zombies = get_Zombies()
if len(zombies) > 0:
	logMessage = 'Amb-Tools: '+str(len(zombies))+' Zombie(s) found: '
	for zomb in zombies:
		logMessage += zomb[3]+'('+zomb[1]+'), '
	logMessage = logMessage[:-1]            #removing last comma of string

	atl.logEvent(logMessage)

	if REBOOT_ON_ZOMBIES:
		atl.logEvent('reboot system...')
		Telegram.send_message(logMessage + '\n' + zombie_emoji+' reboot due to zombie invasion '+zombie_emoji)

		err = os.system('reboot')
		if err != 0:
			atl.logEvent('error: reboot failed! (no permission?)')
			Telegram.send_message('Reboot failed probably due to missing sudo/root permission... Zombies still alive '+scream_emoji+zombie_emoji+zombie_emoji)
	else:
		logEvent('no action performed')
		Telegram.send_message(zombie_emoji + logMessage + '\nrebootOnZombies == False, no action performed!')
else:
	print('no Zombies found...')
