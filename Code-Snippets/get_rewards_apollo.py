import requests
import os
import csv
from time import gmtime, strftime

os.system('ls')

#enter your home directory with your username
home = "/home/yourUserName/"

#enter your node(s) and set active slots below to 1! Slot 1 is always active!

node1 = '0x0000000000000000000000000000000000000000'
node2 = '0x0000000000000000000000000000000000000000'
node3 = '0x0000000000000000000000000000000000000000'
node4 = '0x0000000000000000000000000000000000000000'
node5 = '0x0000000000000000000000000000000000000000'
node6 = '0x0000000000000000000000000000000000000000'

node2active = 0
node3active = 0
node4active = 0
node5active = 0
node6active = 0

#############################################################

nodes = [node1]

if node2active == 1:
    nodes.append(node2)

if node3active == 1:
    nodes.append(node3)

if node4active == 1:
    nodes.append(node4)

if node5active == 1:
    nodes.append(node5)

if node6active == 1:
    nodes.append(node6)

api_url_base = 'https://explorer-api.ambrosus.com/apollos'
count = 0
state = ["a","b","c","d","e","f"]
status = ["a","b","c","d","e","f"]
balance = ["a","b","c","d","e","f"]
for each in nodes:
    print(each)
    response = requests.get(api_url_base)
    data = str(response.json())
    found = (data.split(each))
    search = (len(found))
    while search == 1:
        next = (data.split('next'))
        if (len(next)) < 2:
            status[count] = "OFFLINE"
            balance[count] = 0
            break
        else:
            pageCloseEnd = (next[1].split(','))
            pageCloserEnd = (pageCloseEnd[0].split(': '))
            pageEnd = pageCloserEnd[1]
            pageEnd = (pageEnd.replace("'", ""))
            newlink = ("https://explorer-api.ambrosus.com/apollos?next="+pageEnd)
            #print(newlink)
            response = requests.get(newlink)
            data = str(response.json())
            found = (data.split(each))
            search = (len(found))

    closeBalance = (found[2].split(','))
    closerBalance = (closeBalance[2].split(': '))
    evenCloserBalance = (closerBalance[1].replace("\"", ""))
    evenCloserBalance = (evenCloserBalance.replace("}", ""))
    #balanceRealClose = (evenCloserBalance.split('.'))
    balance[count] = evenCloserBalance

    closerState = (found[1].split('state'))
    evenCloserState = (closerState[1].split(','))
    evenCloserStatenow = (evenCloserState[0].split(': '))
    state[count] = (evenCloserStatenow[1].replace("\"", ""))
    state[count] = (state[count].replace("'", "")) 

    closerStatus = (found[1].split('status'))
    evenCloserStatus = (closerStatus[1].split(","))
    evenCloserStatusnow = (evenCloserStatus[0].split(": "))
    status[count] = (evenCloserStatusnow[1].replace("\"", ""))
    status[count] = (status[count].replace("'", ""))
    
    if state[count] == "RETIRED":
        status[count] = "OFFLINE"
    print(status[count])
    count = count + 1


#change currency to track amb-price in at the very end of the link (for example: USD,EUR,CNY,JPY,CHF,CAD,AUD,GBP,INR,NOK,PLN):

api_url_info = 'https://api.coingecko.com/api/v3/simple/price?ids=amber&vs_currencies=USD'
response = requests.get(api_url_info)
data = str(response.json())
closePrice = (data.split(','))
closerPrice = (closePrice[12].split(':'))
priceusd = (closerPrice[1].replace(" ", ""))


datewrite = strftime("%Y-%m-%d %H:%M:%S", gmtime())
time = strftime("%H%M", gmtime())

if 'buffer' in locals():
    buffer.clear()

if 'buffer' in globals():
    buffer.clear()

buffer = [str(balance[0])+"\n"]

if node2active == 1:
    buffer.append(str(balance[1])+"\n")

if node3active == 1:
    buffer.append(str(balance[2])+"\n")

if node4active == 1:
    buffer.append(str(balance[3])+"\n")

if node5active == 1:
    buffer.append(str(balance[4])+"\n")

if node6active == 1:
    buffer.append(str(balance[5])+"\n")

bufffile = open(home+"buffer.txt","r")
buff = bufffile.readlines()
bufffile.close()
buff[0] = (buff[0].replace("\n", ""))
baldif0 = float(balance[0]) - float(buff[0])
if node2active == 1:
    buff[1] = (buff[1].replace("\n", ""))
    baldif1 = float(balance[1]) - float(buff[1])
if node3active == 1:
    buff[2] = (buff[2].replace("\n", ""))
    baldif2 = float(balance[2]) - float(buff[2])
if node4active == 1:
    buff[3] = (buff[3].replace("\n", ""))
    baldif3 = float(balance[3]) - float(buff[3])
if node5active == 1:
    buff[4] = (buff[4].replace("\n", ""))
    baldif4 = float(balance[4]) - float(buff[4])
if node6active == 1:
    buff[4] = (buff[5].replace("\n", ""))
    baldif5 = float(balance[5]) - float(buff[5])
bufffil = open(home+"buffer.txt","w")
bufffil.writelines(buffer)
bufffil.close()
csvfile = open(home+"rewards.csv","a")
csv0 = ("\"Staking\",\""+str(baldif0)+"\",\"AMB\",\"\",\"\",\"\",\"\",\"\",\"\",\"Apollo Node1\",\""+datewrite+"\",\""+priceusd+"\"\n")
csvfile.writelines(csv0)
if node2active == 1:
    csv1 = ("\"Staking\",\""+str(baldif1)+"\",\"AMB\",\"\",\"\",\"\",\"\",\"\",\"\",\"Apollo Node2\",\""+datewrite+"\",\""+priceusd+"\"\n")
    csvfile.writelines(csv1)
if node3active == 1:
    csv2 = ("\"Staking\",\""+str(baldif2)+"\",\"AMB\",\"\",\"\",\"\",\"\",\"\",\"\",\"Apollo Node3\",\""+datewrite+"\",\""+priceusd+"\"\n")
    csvfile.writelines(csv2)
if node4active == 1:
    csv3 = ("\"Staking\",\""+str(baldif3)+"\",\"AMB\",\"\",\"\",\"\",\"\",\"\",\"\",\"Apollo Node4\",\""+datewrite+"\",\""+priceusd+"\"\n")
    csvfile.writelines(csv3)
if node5active == 1:
    csv4 = ("\"Staking\",\""+str(baldif4)+"\",\"AMB\",\"\",\"\",\"\",\"\",\"\",\"\",\"Apollo Node5\",\""+datewrite+"\",\""+priceusd+"\"\n")
    csvfile.writelines(csv4)
if node6active == 1:
    csv5 = ("\"Staking\",\""+str(baldif5)+"\",\"AMB\",\"\",\"\",\"\",\"\",\"\",\"\",\"Apollo Node6\",\""+datewrite+"\",\""+priceusd+"\"\n")
    csvfile.writelines(csv5)
csvfile.close()
