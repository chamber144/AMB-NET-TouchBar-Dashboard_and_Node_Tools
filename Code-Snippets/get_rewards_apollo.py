#Enter your Settings here:
#------------------------------------------------------------
#enter your home directory with your username
home = "/home/myusername/"

#enter your apollo node(s) in the brackets, seperated by comma and surrounded by inverted commas like this ['0x21...','0x35...','0x64...']

apollonodes = []


#currency to write price into the csv file (for example EUR, CAD, CHF, CNY, RUB, JPY, for available conversions check: https://www.coingecko.com/)
currency = 'USD'

#------------------------------------------------------------



import requests
import os
import csv
from time import gmtime, strftime

count = 0
state = []
status = []
balance = []
for each in apollonodes:
    print(each)
    api_url_base = ('https://explorer-api.ambrosus.com/apollos/'+each)
    response = requests.get(api_url_base)
    data = str(response.json())
    found = (data.split(each))
    search = (len(found))
    if search == 2:
        status = "OFFLINE"
        print('Node is OFFLINE, please wait for sync to complete!')   

    closeBalance = (found[2].split(','))
    closerBalance = (closeBalance[2].split(': '))
    evenCloserBalance = (closerBalance[1].replace("\"", ""))
    evenCloserBalance = (evenCloserBalance.replace("}", ""))
    #balanceRealClose = (evenCloserBalance.split('.'))
    balance.append(evenCloserBalance)

    closerState = (found[1].split('state'))
    evenCloserState = (closerState[1].split(','))
    evenCloserStatenow = (evenCloserState[0].split(': '))
    state.append(evenCloserStatenow[1].replace("\"", ""))
    state[count] = (state[count].replace("'", "")) 

    closerStatus = (found[1].split('status'))
    evenCloserStatus = (closerStatus[1].split(","))
    evenCloserStatusnow = (evenCloserStatus[0].split(": "))
    status.append(evenCloserStatusnow[1].replace("\"", ""))
    status[count] = (status[count].replace("'", ""))
    
    if state[count] == "RETIRED":
        status[count] = "OFFLINE"
    print(status[count])
    count = count + 1

#change currency to track amb-price in at the very end of the link (for example: USD,EUR,CNY,JPY,CHF,CAD,AUD,GBP,INR,NOK,PLN):
api_url_info = ('https://api.coingecko.com/api/v3/simple/price?ids=amber&vs_currencies='+str(currency))
response = requests.get(api_url_info)
data = str(response.json())
closePrice = (data.split(':'))
closerPrice = (closePrice[2].replace("}",""))
priceusd = (closerPrice.replace(" ", ""))


datewrite = strftime("%Y-%m-%d %H:%M:%S", gmtime())
time = strftime("%H%M", gmtime())

if 'buffer' in locals():
    buffer.clear()

if 'buffer' in globals():
    buffer.clear()

count = 0
buffer = []
for each in apollonodes:
    buffer.append(str(balance[count])+"\n")
    count = count + 1

reset = "0"

#function to check if buffer file exists, set it up if necessary.
def buffer_exist(bfile,nodetype):
    val = ""
    try:
        f = open(home+bfile)
    except IOError:
        print("File not accessible creating "+bfile+" !")
        global reset
        reset = "1"
        f = open(home+bfile,"w")
        count = 0
        for each in nodetype:
            if count == len(nodetype)-1:
                val = (val+"0")
            else:
                val = (val+"0\n")
            count = count + 1
        f.writelines(val)
    finally:
        f.close()

#function to check if nodes are correctly registered in buffer file, reset if needed and read.
def buffer_slots(bfile,nodetype,nodename,type):
    f = open(home+bfile,"r")
    readtxt = f.readlines()
    f.close()
    val = ""
    if len(nodetype) != len(readtxt):
        print("Number of "+nodename+" has changed, resetting "+type+" file!")
        global reset
        reset = "1"
        f = open(home+bfile,"w")
        count = 0
        for each in nodetype:
            if count == len(nodetype)-1:
                val = (val+"0")
            else:
                val = (val+"0\n")
            count = count + 1
        f.writelines(val)
        f.close()
        return reset

buffer_exist("buffer.txt",apollonodes)
buffer_slots("buffer.txt",apollonodes,"Apollo Nodes","buffer")

bufffile = open(home+"buffer.txt","r")
buff = bufffile.readlines()
bufffile.close()

count = 0
csvfile = open(home+"rewards.csv","a")
for each in apollonodes:
    buff[count] = (buff[count].replace("\n", ""))
    baldif = (float(balance[count]) - float(buff[count]))
    transfer = ""
    if baldif < 0:
        transfer = "It seems you have transfered funds manually that need to be added to the balance!"
    csv = ("\"Staking\",\""+str(baldif)+"\",\"AMB\",\"\",\"\",\"\",\"\",\"\",\""+transfer+"\",\"Apollo Node"+str(count+1)+"\",\""+datewrite+"\",\""+priceusd+"\"\n")
    csvfile.writelines(csv)
    count = count + 1
csvfile.close()

bufffil = open(home+"buffer.txt","w")
bufffil.writelines(buffer)
bufffil.close()
