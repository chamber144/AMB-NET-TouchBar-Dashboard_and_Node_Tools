# Ambtools library: Collection of functions used by more than one module
import os
import yaml
from datetime import datetime

#TODO: test exceptions. iirc it wasn't working as expected.
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

def logEvent(msg, logFile):
	print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + ': ' + msg, file=open(logFile, 'a'))

