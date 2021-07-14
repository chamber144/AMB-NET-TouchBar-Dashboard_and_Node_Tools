#-----------------------------------------------------------------

#set a name for this node (this name is used in the csv file and is essential to differentiate different nodes values later)
nodename = 'AtlasNode1'

#set this nodes public address
account = '0x0000000000000000000000000000000000000000'

#enter your home directory with your username or if you are on root, the root directory (check with the pwd command) be sure to have a / in the end
home = '/root/'

#After invoking payout-action, send the funds to another account? (1 = yes, 0 = no)
sendAMBout = 0

#If you choose to send out Payout funds to another account, enter your other amb-net address to send payout funds to:
#Be sure to check the address is correct, otherwise your funds will be lost!!!
sendtoaddress = '0x0000000000000000000000000000000000000000'

#Amb to keep in account for fees after sending payout funds to the other address:
ambtokeep = 50

#This nodes private key to be able to send the transactions.
key = '0x0000000000000000000000000000000000000000000000000000000000000000'

#currency to write price into the csv file (for example EUR, CAD, CHF, CNY, RUB, JPY, for available conversions check: https://www.coingecko.com/)
currency = 'USD'
       

#seconds to wait for payout transaction to go through before calculating balance to send to other address
#As AMB-net gets used more over time, this may have to be raised in the future.
waittime = 10

#Option to raise transaction gas Limit x times
gasLimitMultiplicator = 1


#-----------------------------------------------------------------

import requests
import time
import os
import csv
import json
from time import gmtime, strftime

from web3 import Web3, HTTPProvider
web3 = Web3(HTTPProvider("http://localhost:8545"))

#account = web3.eth.coinbase

api_url_base = ('https://explorer-api.ambrosus.io/atlases/'+account)
response = requests.get(api_url_base)
data = str(response.json())
found = (data.split(account))
search = (len(found))
if search == 2:
    status = "OFFLINE"
    print('Node is OFFLINE, please wait for sync to complete!')   

getPayout = (found[1].split('payPeriods'))
closerGetPayout = (getPayout[1].split(','))
evenCloserGetPayout = (closerGetPayout[1].split(': '))
availablePayout = (evenCloserGetPayout[1].replace(" ", ""))

blocknumber  = web3.eth.blockNumber
gasprice =  web3.eth.gasPrice
chainid = web3.eth.chainId

print('Your Account: '+str(account))
print('Available Payout: '+str(availablePayout))
print('AMB-Net Blocknumber: '+str(blocknumber))
print('Your old Balance: '+str(web3.fromWei(web3.eth.getBalance(account), 'ether')))

#calculate gas for regular transaction
gasToUse = web3.eth.estimateGas({'to': sendtoaddress, 'from': account, 'value': 1000000000000000000000000})

#to generate the data needed to invoke the payout function, the first two chars 0x need to be stripped from the address
result_str = ''
for i in range(0, len(account)): 
    if i >= 2: 
        result_str = result_str + account[i] 
accountStripped = result_str

#the stripped down address is attached at the end of the following data for the complete data-string
dataforpayout = ('0x51cff8d9000000000000000000000000'+accountStripped)

#sign the payout transaction to the ambrosus smart contract
signed_payouttxn = web3.eth.account.signTransaction(dict(
    nonce=web3.eth.getTransactionCount(account),
    gasPrice=web3.eth.gasPrice,
    gas=gasToUse*300*gasLimitMultiplicator,
    to='0x77C70B382bEf2Ff2D01E25902d0D338586b51Df6',
    value=0,
    data=dataforpayout,
  ),
  key,
)

#function to check if buffer file exists, set it up if necessary.
def buffer_exist(bfile):
    val = ""
    try:
        f = open(home+bfile)
    except IOError:
        print("File not accessible creating "+bfile+" !")
        global reset
        reset = "1"
        f = open(home+bfile,"w")
        val = "0"        
        f.writelines(val)
    finally:
        f.close()

buffer_exist("bufferbalance.txt")

balfile = open(home+"bufferbalance.txt","r")
balat = balfile.readlines()
balfile.close()
count = 0 
for each in balat:
    balat[count] = (balat[count].replace("\n", ""))
    count = count + 1

oldbalance = web3.fromWei(web3.eth.getBalance(account), 'ether')
fees = round(float(balat[0]), 5) - round(float(oldbalance), 5)
if fees < 0:
    fees = 0              

#send signed payout contract transaction
if str(availablePayout) != "0":
    web3.eth.sendRawTransaction(signed_payouttxn.rawTransaction)
    print('Payout transaction sent!')
    #wait for transaction to go through
    print('Waiting '+str(waittime)+' seconds to be safe the payout has been executed!')      
    time.sleep(waittime)
    print('Your new Balance: '+str(web3.fromWei(web3.eth.getBalance(account), 'ether')))                      
else:
    print('No Payout is available')

balance = web3.eth.getBalance(account)
keepinaccount = web3.toWei(ambtokeep, 'ether')
tosendbalance = int(balance) - int(keepinaccount)
if tosendbalance <= 0:
    tosendbalance = 0
    ambtosend = 0
else:    
    ambtosend = web3.fromWei(tosendbalance, 'ether')

#sign the amb transaction
signed_txn = web3.eth.account.signTransaction(dict(
    nonce=web3.eth.getTransactionCount(account),
    gasPrice=web3.eth.gasPrice,
    gas=gasToUse*gasLimitMultiplicator,
    to=sendtoaddress,
    value=tosendbalance,
    data=b'',
  ),
  key,
)

#write buffer to be able to calculate fees
if str(sendAMBout) == "0":
        f = open(home+"bufferbalance.txt","w")      
        f.writelines(str(web3.fromWei(web3.eth.getBalance(account), 'ether')))
        f.close()
else:
        f = open(home+"bufferbalance.txt","w")      
        f.writelines(str(ambtokeep))
        f.close()

#send signed amb transaction
if str(sendAMBout) == "1":
    if str(availablePayout) != "0":
        web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(str(ambtosend)+' AMB sent out to the following account: '+str(sendtoaddress))
    else:
        print('No Payout, no funds to send!')

#pull price info from coingecko API
api_url_info = ('https://api.coingecko.com/api/v3/simple/price?ids=amber&vs_currencies='+str(currency))
response = requests.get(api_url_info)
data = str(response.json())
closePrice = (data.split(':'))
closerPrice = (closePrice[2].replace("}",""))
priceusd = (closerPrice.replace(" ", ""))

datewrite = strftime("%Y-%m-%d %H:%M:%S", gmtime())
time = strftime("%H%M", gmtime())

transfer = ""
if fees >= 1000:
    transfer = "It seems you have transfered funds manually that need to be deducted from fees!"

if str(availablePayout) == "0":
    print('No Payout available to write to csv file')
else:
    csvfile = open(home+"rewards_"+str(nodename)+".csv","a")
    csv0 = ("\"Staking\",\""+str(availablePayout)+"\",\"AMB\",\"\",\"\",\"\",\"\",\"\",\"\",\""+nodename+"\",\""+datewrite+"\",\""+priceusd+"\"\n")
    csvfile.writelines(csv0)
    csvfile.close()
    print('Payout written to csv file')
    csvfile2 = open(home+"fees_"+str(nodename)+".csv","a")
    csv1 = ("\"Fees\",\""+str(fees)+"\",\"AMB\",\"\",\"\",\"\",\"\",\"\",\""+transfer+"\",\""+nodename+"\",\""+datewrite+"\",\""+priceusd+"\"\n")
    csvfile2.writelines(csv1)
    csvfile2.close()
    print('Fees written to csv file')
