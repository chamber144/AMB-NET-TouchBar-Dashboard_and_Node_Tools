#Amb-Net Telegram Notification v3.2 2022January22
#Enter your Settings here:
#------------------------------------------------------------


#enter your home directory with your username or if you are on root, the root directory (check with the pwd command) be sure to have a / in the end
home = '/root/'

#enter your Telegram Token and chat id
Telegram_Token = ''
Telegram_Chat_ID = ''

#enter your atlas node(s) in the brackets, separated by comma and surrounded by inverted commas like this ['0x21...','0x35...','0x64...']
atlasnodes = []

#enter your apollo node(s) in the brackets, separated by comma and surrounded by inverted commas like this ['0x21...','0x35...','0x64...']
apollonodes = []


#Send daily status message? (1 = yes, 0 = no)
statusmessage = '1'
#Set (server)time when to send daily status message
statstime = '1505'
#show rewards in currency of choice? For Atlas, amount of AMB and currency are shown. This has to be split into 13 Payouts. (1 = yes, 0 = no)
calculateFiat = '1'
#currency to write price into the daily status message (for example EUR, CAD, CHF, CNY, RUB, JPY, for available conversions check: https://www.coingecko.com/)
currency = 'USD'
#Show Hermes updates with daily status message? (1 = yes, 0 = no)
hermesinfo = '1'
#Hide new Heartbeat Bundles on AMB-NET and TEST-NET in daily status message? (1 = yes, 0 = no)
hideHeartbeat = '1'
#Hide new TEST-NET Bundles in daily status message? (1 = yes, 0 = no)
hideTestnet = '0'


#to set Bundle Warnings, enter as many values as you'd like to be notified at, seperated by comma and surrounded by inverted commas like this ['100','200','1000']
dailybundlewarnings = ['60','100','125','150','200','300','400','500','600','700','800','900','1000','5000']

#once a daily-bundles value has triggered a warning, how much lower does the value need to go, until it can be triggered again?
#without this mechanism, notifications would be sent repeatedly, if you get too many Bundle Warnings, raise the following value:
sensitivity = '10'

#cryptonomics - only change if cryptonomics change
bundlecostusd = 8
treasury = 0.7
#---------------------------------------------------------------

import requests
import random
import os.path
from time import gmtime, strftime
import datetime
from decimal import Decimal,ROUND_HALF_UP

nodeOffline = '\U0001f6a8'
nodeOnline = '\u2705'
lowBalance = '\u26A0\uFE0F'
celeb1 = '\U0001F389'
celeb2 = '\U0001F973'
celeb3 = '\U0001F37E'

#atlas reward calculation (split to 7 atlas nodes in the end)
atlasrewardfactor = 0.7 * treasury * 0.1428571429

#get time
time = strftime("%H%M", gmtime())
datewrite = strftime("%Y-%m-%d", gmtime())

datetimenow = datetime.datetime.now()
date = datetimenow.strftime('%Y-%m-%d')
year = datetimenow.year
month = datetimenow.month
day = datetimenow.day
d3 = datetime.date(year, month, day)
d1 = datetime.date(2020, 12, 24)
i = 0
while i == 0:
        d2 = d1 + datetime.timedelta(days=28)
        payoutdate = d2.strftime('%Y-%m-%d')
        if date == payoutdate:
                payout = ("Payout = "+payoutdate+" (Today !)\n")
                break
        elif date > payoutdate:
                d1 = d2       
        else:
                d4 = d2 - d3
                futuredate = d4.days
                payout = ("Payout = "+payoutdate+" (in "+str(futuredate)+" days)\n")
                break



folder = 'telegram_notification_buffers/'

#check if folder for buffer files exists, create, if not.
if os.path.isdir(home+folder):
    print ("")   
else:
    print ("Folder not accessible creating telegram_notification_buffers folder !")
    os.mkdir(home+folder)


reset = "0"

#function to check if buffer file exists, set it up if necessary.
def buffer_exist(bfile,nodetype):
    val = ""
    try:
        f = open(home+folder+bfile)
    except IOError:
        print("File not accessible creating "+bfile+" !")
        global reset
        reset = "1"
        f = open(home+folder+bfile,"w")
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
    f = open(home+folder+bfile,"r")
    readtxt = f.readlines()
    f.close()
    val = ""
    if len(nodetype) != len(readtxt):
        print("Number of "+nodename+" has changed, resetting "+type+" file!")
        global reset
        reset = "1"
        f = open(home+folder+bfile,"w")
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

buffer_exist("bundlebuffer.txt",dailybundlewarnings)
buffer_slots("bundlebuffer.txt",dailybundlewarnings,"Bundle Warnings","buffer")    

hermes_url = 'https://explorer-api.ambrosus.io/hermeses'
hermes_test = 'https://explorer-api.ambrosus-test.io/hermeses'

#get Amb-net Hermes Data
response = requests.get(hermes_url)
dataraw = str(response.json())

nextherm = (dataraw.split('hasNext'))
nexthermm = (nextherm[1].split(','))
nexthermmm = (nexthermm[0].replace('\': ', ''))
while nexthermmm == "true":
    pageCloseEnd = (nexthermm[1].split(': '))
    pageEnd = (pageCloseEnd[1].replace('\'', ''))
    newHermesLink = (hermes_url+"?next="+pageEnd)
    #print(newHermesLink)
    response = requests.get(newHermesLink)
    data = str(response.json())
    nextherm = (data.split('hasNext'))
    nexthermm = (nextherm[1].split(','))
    nexthermmm = (nexthermm[0].replace('\': ', ''))
    dataraw = dataraw+data

closeBundles = (dataraw.split('totalBundles'))
countit = 0
hermesBundles = []
hermesNames = []
for each in closeBundles:
    closerBundless = (closeBundles[countit].split(': '))
    closerBundles = (closerBundless[1].split(','))
    hermesBundles.append(closerBundles[0].replace("'", ""))
    closerName = (closerBundless[2].split(','))
    hermesNames.append(closerName[0].replace("'", ""))
    countit = countit + 1

hermesNames.pop(0)
hermesBundles.pop(0)
print(hermesNames)                            
print(hermesBundles)

closeAddress = (dataraw.split('address'))
countit = 0
countherm = 0
hermesAddress = []
for each in closeAddress:
    closerAddresss = (closeAddress[countit].split(': '))
    closerAddress = (closerAddresss[1].split(','))
    hermesAddress.append(closerAddress[0].replace("'", ""))
    if len(hermesAddress) >= 3:
        if hermesAddress[countherm-1] == hermesAddress[countherm]:
            hermesAddress.pop(countherm)
            countherm = countherm - 1
    countherm = countherm + 1       
    countit = countit + 1
hermesAddress.pop(0)
#print(len(hermesAddress))

#get Test-Net Hermes Data
response = requests.get(hermes_test)
dataraw = str(response.json())

nextherm = (dataraw.split('hasNext'))
nexthermm = (nextherm[1].split(','))
nexthermmm = (nexthermm[0].replace('\': ', ''))
while nexthermmm == "true":
    pageCloseEnd = (nexthermm[1].split(': '))
    pageEnd = (pageCloseEnd[1].replace('\'', ''))
    newTestHermesLink = (hermes_test+"?next="+pageEnd)
    #print(newTestHermesLink)
    response = requests.get(newTestHermesLink)
    data = str(response.json())
    nextherm = (data.split('hasNext'))
    nexthermm = (nextherm[1].split(','))
    nexthermmm = (nexthermm[0].replace('\': ', ''))
    dataraw = dataraw+data


closeBundles = (dataraw.split('totalBundles'))
countit = 0
hermesTestBundles = []
hermesTestNames = []
for each in closeBundles:
    closerBundless = (closeBundles[countit].split(': '))
    closerBundles = (closerBundless[1].split(','))
    hermesTestBundles.append(closerBundles[0].replace("'", ""))
    closerName = (closerBundless[2].split(','))
    hermesTestNames.append(closerName[0].replace("'", ""))
    countit = countit + 1

hermesTestNames.pop(0)
hermesTestBundles.pop(0)
print(hermesTestNames)                            
print(hermesTestBundles)    

closeTestAddress = (dataraw.split('address'))
countit = 0
countherm = 0
hermesTestAddress = []
for each in closeTestAddress:
    closerTestAddresss = (closeTestAddress[countit].split(': '))
    closerTestAddress = (closerTestAddresss[1].split(','))
    hermesTestAddress.append(closerTestAddress[0].replace("'", ""))
    if len(hermesTestAddress) >= 3:
        if hermesTestAddress[countherm-1] == hermesTestAddress[countherm]:
            hermesTestAddress.pop(countherm)
            countherm = countherm - 1
    countherm = countherm + 1       
    countit = countit + 1
hermesTestAddress.pop(0)
#print(len(hermesTestAddress))

#function to check if Hermes buffer file exists, set it up if necessary.
def bufferhermes_exist(bfiles,hermesNames,hermesBundles):
    val = ""
    try:
        f = open(home+folder+bfiles)
    except IOError:
        print("File not accessible creating "+bfiles+" !")
        global reset
        reset = "1"
        f = open(home+folder+bfiles,"w")
        count = 0
        for each in hermesNames:
            if count == len(hermesNames)-1:
                val = (val+hermesNames[count]+"\n"+hermesBundles[count])
            else:
                val = (val+hermesNames[count]+"\n"+hermesBundles[count]+"\n")
            count = count + 1
        f.writelines(val)
    finally:
        f.close()

bufferhermes_exist("hermes.txt",hermesNames,hermesBundles)
bufferhermes_exist("hermesTest.txt",hermesTestNames,hermesTestBundles)


#check if atlas buffer files are setup correctly and read values
if (len(atlasnodes)) > 0:

    buffer_exist("statsatlas.txt",atlasnodes)
    buffer_exist("atlasbuffer.txt",atlasnodes)

    buffer_slots("statsatlas.txt",atlasnodes,"Atlas Nodes","status")
    buffer_slots("atlasbuffer.txt",atlasnodes,"Atlas Nodes","buffer")

    statsfile = open(home+folder+"statsatlas.txt","r")
    statsat = statsfile.readlines()
    statsfile.close()
    count = 0 
    for each in statsat:
        statsat[count] = (statsat[count].replace("\n", ""))
        count = count + 1

#check if apollo buffer files are setup correctly and read values
if (len(apollonodes)) > 0:

    buffer_exist("statsapollo.txt",apollonodes)
    buffer_exist("apollobuffer.txt",apollonodes)

    buffer_slots("statsapollo.txt",apollonodes,"Apollo Nodes","status")
    buffer_slots("apollobuffer.txt",apollonodes,"Apollo Nodes","buffer")    

    statsfile = open(home+folder+"statsapollo.txt","r")
    statsap = statsfile.readlines()
    statsfile.close()
    count = 0
    for each in statsap:
        statsap[count] = (statsap[count].replace("\n", ""))
        count = count + 1

writeatlasbuffer = []
writeapollobuffer = []


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


#get atlas status

count = 0
stateatlas = []
statusatlas = []
bundlesatlas = []
balanceatlas = []
Sat = []
writeatlasbundlebuffer = []
iconatlas = []
for each in atlasnodes:
    print("Atlas "+each)
    api_url_base = ('https://explorer-api.ambrosus.io/atlases/'+each)
    response = requests.get(api_url_base)
    data = str(response.json())
    found = (data.split(each))
    search = (len(found))
    if search == 2:
        status = "OFFLINE"
        print('Node is OFFLINE, please wait for sync to complete!')

    closerBundle = (found[1].split('totalBundles'))
    evenCloserBundle = (closerBundle[1].split(','))
    evenCloserBundlenow = (evenCloserBundle[0].split(': '))
    bundlesatlas.append(evenCloserBundlenow[1].replace("\"", ""))
    writeatlasbundlebuffer.append(bundlesatlas[count]+"\n") 

    closerBalance = (found[1].split('balance'))
    evenCloserBalance = (closerBalance[1].split(','))
    evenCloserBalancenow = (evenCloserBalance[1].split(': '))
    balanceatlas.append(evenCloserBalancenow[1].replace("\"", ""))
    balanceatlas[count] = (balanceatlas[count].replace("}", ""))
    feebalance =  float(balanceatlas[count])

    closerState = (found[1].split('state'))
    evenCloserState = (closerState[1].split(','))
    evenCloserStatenow = (evenCloserState[0].split(': '))
    stateatlas.append(evenCloserStatenow[1].replace("\"", ""))
    stateatlas[count] = (stateatlas[count].replace("'", "")) 
    if stateatlas[count] == "ONBOARDED":
        statusatlas.append("ONLINE")
    else:
        statusatlas.append("OFFLINE")
    print(statusatlas[count])
    if statusatlas[count] != "ONLINE" and statsat[count] == "1":
        send_message(nodeOffline+" Your Atlas Node "+str(count+1)+" has just gone offline! <a href=\"https://explorer.ambrosus.io/atlas/"+each+"\">"+each+"</a>\n\n-------------------------------")
    if statusatlas[count] == "ONLINE" and statsat[count] == "0":
        send_message(nodeOnline+" Your Atlas Node "+str(count+1)+" is back online! <a href=\"https://explorer.ambrosus.io/atlas/"+each+"\">"+each+"</a>\n\n-------------------------------")
    if feebalance <= 10:
        print('Atlas balance is low: '+str(feebalance)) 
        send_message(lowBalance+" Your Atlas Node "+str(count+1)+" has a very low balance of "+ str(feebalance)+" AMB.\n\nFunds might soon not be sufficient to pay the nodes challenge transactions.\nPlease raise the balance: <a href=\"https://explorer.ambrosus.io/atlas/"+each+"\">"+each+"</a>\n\n-------------------------------")
    if statusatlas[count] == "ONLINE":
        Sat.append("1")
        iconatlas.append(nodeOnline)
    else:
        Sat.append("0")            
        iconatlas.append(nodeOffline)
    writeatlasbuffer.append(Sat[count]+"\n",)
    count = count + 1


#get apollo status
    
count = 0
stateapollo = []
statusapollo = []
balanceapollo = []
Sap = []
writeapollobalancebuffer = []
iconapollo = []
for each in apollonodes:
    print("Apollo "+each)
    api_url_base = ('https://explorer-api.ambrosus.io/apollos/'+each)
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
    balanceapollo.append(evenCloserBalance)        
    writeapollobalancebuffer.append(balanceapollo[count]+"\n")    

    closerState = (found[1].split('state'))
    evenCloserState = (closerState[1].split(','))
    evenCloserStatenow = (evenCloserState[0].split(': '))
    stateapollo.append(evenCloserStatenow[1].replace("\"", ""))
    stateapollo[count] = (stateapollo[count].replace("'", "")) 

    closerStatus = (found[1].split('status'))
    evenCloserStatus = (closerStatus[1].split(","))
    evenCloserStatusnow = (evenCloserStatus[0].split(": "))
    statusapollo.append(evenCloserStatusnow[1].replace("\"", ""))
    statusapollo[count] = (statusapollo[count].replace("'", ""))
    
    if stateapollo[count] == "RETIRED":
        statusapollo[count] = "OFFLINE"
    
    print(statusapollo[count])
    if statusapollo[count] != "ONLINE" and statsap[count] == "1":
        send_message(nodeOffline+" Your Apollo Node "+str(count+1)+" has just gone offline! <a href=\"https://explorer.ambrosus.io/apollo/"+each+"\">"+each+"</a>\n\n-------------------------------")
    if statusapollo[count] == "ONLINE" and statsap[count] == "0":
        send_message(nodeOnline+" Your Apollo Node "+str(count+1)+" is back online! <a href=\"https://explorer.ambrosus.io/apollo/"+each+"\">"+each+"</a>\n\n-------------------------------")
    if statusapollo[count] == "ONLINE":
        Sap.append("1")
        iconapollo.append(nodeOnline)
    else:
        Sap.append("0")
        iconapollo.append(nodeOffline)
    writeapollobuffer.append(Sap[count]+"\n")        
    count = count + 1


if (len(atlasnodes)) > 0:
    statsfile = open(home+folder+"statsatlas.txt","w")
    statsat = statsfile.writelines(writeatlasbuffer)
    statsfile.close()

if (len(apollonodes)) > 0:    
    statsfile = open(home+folder+"statsapollo.txt","w")
    statsap = statsfile.writelines(writeapollobuffer)
    statsfile.close()

if reset == "1":
    if (len(atlasnodes)) > 0:
        statsfile = open(home+folder+"atlasbuffer.txt","w")
        statsat = statsfile.writelines(writeatlasbundlebuffer)
        statsfile.close()

    if (len(apollonodes)) > 0:    
        statsfile = open(home+folder+"apollobuffer.txt","w")
        statsap = statsfile.writelines(writeapollobalancebuffer)
        statsfile.close()


#get network stats
api_url_info = 'https://explorer-api.ambrosus.io/info'
response = requests.get(api_url_info)
data = str(response.json())
closeBundles = (data.split(','))
closerBundles = (closeBundles[32].split(':'))
networkBundles = (closerBundles[1].replace(" ", ""))

closerBlockTransactions = (closeBundles[29].split(':'))
AverageBlockTransactions = (closerBlockTransactions[1].replace(" ", ""))
AverageBlockTransactions = Decimal(AverageBlockTransactions).quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)

closerBundleCost = (closeBundles[22].split(':'))
Bundlecost = (closerBundleCost[1].replace(" ", ""))
Bundlecost = (Bundlecost.replace("}", ""))

closerAtlasStake = (closeBundles[11].split(':'))
AtlasStake = (closerAtlasStake[1].replace(" ", ""))
AtlasStake = (AtlasStake.replace("}", ""))

closerApolloStake = (closeBundles[9].split(':'))
ApolloStake = (closerApolloStake[1].replace(" ", ""))
ApolloStake = (ApolloStake.replace("}", ""))

AllStake = float(AtlasStake) + float(ApolloStake)

closeratlas = (closeBundles[16].split(':'))
atlasnum = (closeratlas[2].replace(" ", ""))
atlasnum = (atlasnum.replace("}", ""))

closerapollo = (closeBundles[13].split(':'))
apollonum = (closerapollo[1].replace(" ", ""))
apollonum = (apollonum.replace("}", ""))

closerhermes = (closeBundles[17].split(':'))
hermesnum = (closerhermes[2].replace(" ", ""))
hermesnum = (hermesnum.replace("}", ""))

#get projected future bundle price
api_internalprice_url='https://token.ambrosus.io/price'
totalprice = 0
nextcost = 0
response = requests.get(api_internalprice_url)
data = str(response.json())
lines=data.split(',')
for line in lines:
        if '\'total_price_usd\':' in line:
                if 'None' in line:
                        nextcost = 0.00
                else:
                        wk1=line.split(': ')
                        totalpricewk=wk1[1][1:-1]
                        totalprice=Decimal(totalpricewk)
                        nextcost=bundlecostusd/totalprice
                        nextcost = Decimal(nextcost).quantize(Decimal("1"),rounding=ROUND_HALF_UP)

#change currency to track amb-price in at the very end of the link (for example: USD,EUR,CNY,JPY,CHF,CAD,AUD,GBP,INR,NOK,PLN):
api_url_info = ('https://api.coingecko.com/api/v3/simple/price?ids=amber&vs_currencies='+str(currency))
response = requests.get(api_url_info)
data = str(response.json())
closePrice = (data.split(':'))
closerPrice = (closePrice[2].replace("}",""))
price = (closerPrice.replace(" ", ""))


if currency == "USD":
    currency = "$"
elif currency == "EUR":
    currency = "€"
elif currency == "JPY":
    currency = "¥"
elif currency == "CNY":
    currency = "¥"
elif currency == "RUB":
    currency = "₽"  

#check for Bundle warnings to trigger
f = open(home+folder+"bundlebuffer.txt","r")
bundletriggers = f.readlines()
f.close()
count = 0
trig = "0"
for each in bundletriggers:
    bundletriggers[count] = (bundletriggers[count].replace("\n", ""))
    if int(networkBundles) < int(dailybundlewarnings[count])-int(sensitivity):
        if bundletriggers[count] == "1":
            trig = "1"
            bundletriggers[count] = "0"
    if int(networkBundles)>(int(dailybundlewarnings[count])*10):
        print("Likely an explorer glitch, seems to be a too steep rise in bundles!")
    else:    
        if int(networkBundles) >= int(dailybundlewarnings[count]):
            if bundletriggers[count] == "0":
                if int(networkBundles) >= 5000:
                        send_message(celeb2+" Daily Bundles value raised \nabove "+str(dailybundlewarnings[count])+" to "+str(networkBundles)+" "+celeb3+"\n"+celeb3+celeb3+celeb3+celeb3+celeb3+celeb3+celeb3+celeb3+celeb3+celeb3+"\n-------------------------------")
                elif int(networkBundles) >= 1000:
                        send_message(celeb1+" Daily Bundles value raised \nabove "+str(dailybundlewarnings[count])+" to "+str(networkBundles)+" "+celeb2+"\n-------------------------------")
                else:
                        send_message(celeb1+" Daily Bundles value raised \nabove "+str(dailybundlewarnings[count])+" to "+str(networkBundles)+" "+celeb1+"\n-------------------------------")
                trig = "1"
                bundletriggers[count] = "1" 
    count = count + 1

if trig == "1":
    count = 0
    val = ""
    for each in bundletriggers:
        if count == len(bundletriggers)-1:
            val = (val+bundletriggers[count])
        else:
            val = (val+bundletriggers[count]+"\n")
        count = count + 1
    f = open(home+folder+"bundlebuffer.txt","w")
    f.writelines(val)
    f.close()

#Daily Overview and network statistics
if time == statstime:
        baldifallapollo = 0
        baldifapollo = []
        apollostring = ""
        balanceall = 0
        if (len(apollonodes)) > 0:
            bufffile = open(home+folder+"apollobuffer.txt","r")
            count = 0
            buff = bufffile.readlines()
            bufffile.close()
            for each in buff:
                buff[count] = (buff[count].replace("\n", ""))
                baldifapollo.append(float(balanceapollo[count]) - float(buff[count]))
                baldifallapollo = baldifallapollo + baldifapollo[count]
                balanceall = balanceall + float(balanceapollo[count])
                allfiat = float(balanceall) * float(price)
                allfiat = Decimal(allfiat).quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)
                newfiat = float(baldifallapollo) * float(price)
                newfiat = Decimal(newfiat).quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)
                fiat = ("                      "+str(int(allfiat))+" new: ~"+str(newfiat)+" "+currency+"\n")
                if calculateFiat != "1":
                    fiat = ""
                apollostring = (apollostring+"<a href=\"https://explorer.ambrosus.io/apollo/"+str(apollonodes[count])+"\">Apollo "+str(count+1)+"</a>  "+str(iconapollo[count])+"\t "+str(int(float(balanceapollo[count])))+"\t new: "+str(int(float(baldifapollo[count])))+" AMB\n")
                count = count + 1
            apollostring = (apollostring+"                      –––––––––––––––––––\n                      "+str(int(balanceall))+" new: "+str(int(baldifallapollo))+" AMB\n"+str(fiat))
            
        baldifallatlas = 0
        baldifatlas = []
        atlasstring = ""
        bundleall = 0
        if (len(atlasnodes)) > 0:
            bufffile = open(home+folder+"atlasbuffer.txt","r")
            count = 0
            buff = bufffile.readlines()
            bufffile.close()
            for each in buff:
                buff[count] = (buff[count].replace("\n", ""))
                baldifatlas.append(int(bundlesatlas[count]) - int(buff[count]))
                baldifallatlas = baldifallatlas + baldifatlas[count]
                bundleall = bundleall + (int(bundlesatlas[count]))
                bunber = str(Bundlecost)
                bunber = int(bunber)
                ambrewards = bunber * float(baldifallatlas) * float(atlasrewardfactor)
                ambrewardsss = ("                                      ~"+str(int(ambrewards))+" AMB\n")
                newfiat = float(price) * ambrewards
                newfiat = Decimal(newfiat).quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)
                fiat = ("                                      ~"+str(newfiat)+" "+currency+"\n")
                if calculateFiat != "1":
                    fiat = ""
                    ambrewardsss = ""
                hint = ("                     split into 13 Payouts\n")
                hint = ""
                atlasstring = (atlasstring+"<a href=\"https://explorer.ambrosus.io/atlas/"+str(atlasnodes[count])+"\">Atlas "+str(count+1)+"</a>  "+str(iconatlas[count])+"\t "+str(int(float(bundlesatlas[count])))+"\tnew: "+str(int(float(baldifatlas[count])))+" Bundles\n")
                count = count + 1
            atlasstring = (atlasstring+"                     –––––––––––––––––––\n                     "+str(bundleall)+" new: "+str(baldifallatlas)+" Bundles\n"+str(ambrewardsss)+str(fiat)+str(hint))

#Get hermes information and add to daily status message
      
        #open hermes buffer
        f = open(home+folder+"hermes.txt","r")
        hermes = f.readlines()
        f.close()
        count = 0
        string = ""
        hermesList = []
        hermesAddressList = []
        for each in hermes:
            hermes[count] = (hermes[count].replace("\n", ""))
            countherm = 0
            for info in hermesNames:
                if hermes[count] == hermesNames[countherm]:
                    if hideHeartbeat == "1":
                        if hermes[count] == "https://hermes0.ambrosus.io":
                            print("Ignoring Heartbeat Hermes 0")
                        elif hermes[count] == "https://hermes1.ambrosus.io":
                            print("Ignoring Heartbeat Hermes 1")
                        elif hermes[count] == "https://hermes2.ambrosus.io":
                            print("Ignoring Heartbeat Hermes 2")
                        elif hermes[count] == "https://hermes3.ambrosus.io":
                            print("Ignoring Heartbeat Hermes 3")
                        else:
                            counta = count + 1
                            diff = int(hermesBundles[countherm]) - int(hermes[counta])
                            if int(diff) > 0:
                                celeb = ''
                                if int(diff) >= 1 and int(diff) <= 4:
                                    celeb = '\U0001F331'
                                elif int(diff) >= 5 and int(diff) <= 99:    
                                    celeb = '\U0001F389'
                                elif int(diff) >= 100 and int(diff) <= 499:    
                                    celeb = '\U0001F37E'
                                elif int(diff) >= 500 and int(diff) <= 999:    
                                    celeb = '\U0001F386'
                                elif int(diff) >= 1000:   
                                    celeb = '\U0001F451'
                                name = hermesNames[countherm].split('//')    
                                string = (string+"\n<a href=\"https://explorer.ambrosus.io/address/"+hermesAddress[countherm]+"\">"+name[1]+"</a>\n"+"New Bundles: "+str(diff)+celeb)  
                    else:
                        counta = count + 1
                        diff = int(hermesBundles[countherm]) - int(hermes[counta])
                        if int(diff) > 0:
                            celeb = ''
                            if int(diff) >= 1 and int(diff) <= 4:
                                celeb = '\U0001F331'
                            elif int(diff) >= 5 and int(diff) <= 99:    
                                celeb = '\U0001F389'
                            elif int(diff) >= 100 and int(diff) <= 499:    
                                celeb = '\U0001F37E'
                            elif int(diff) >= 500 and int(diff) <= 999:    
                                celeb = '\U0001F386'
                            elif int(diff) >= 1000:   
                                celeb = '\U0001F451'
                            name = hermesNames[countherm].split('//')      
                            string = (string+"\n<a href=\"https://explorer.ambrosus.io/address/"+hermesAddress[countherm]+"\">"+name[1]+"</a>\n"+"New Bundles: "+str(diff)+celeb)
                countherm = countherm + 1
            count = count + 1

        #overwrite hermes buffer
        f = open(home+folder+"hermes.txt","w")
        text = ""
        count = 0
        for each in hermesNames:
            if count == len(hermesNames)-1:
                text = (text + hermesNames[count]+"\n"+hermesBundles[count])
            else:
                text = (text + hermesNames[count]+"\n"+hermesBundles[count]+"\n")
            count = count + 1

        f.writelines(text)
        f.close()

        count = 0
        for each in hermes:
            countherm = 0
            for info in hermesNames:
                try:
                    if hermes[count] == hermesNames[countherm]:
                        hermesNames.pop(countherm)
                        hermesAddress.pop(countherm)
                except IndexError:
                    print("")
                countherm = countherm + 1
            count = count + 1

        if string != "":
            string = ("\n\nAMB-NET Hermes:"+string)
        if len(hermesNames) > 0:
            count = 0
            string = (string+"\n\nNew Hermes"+celeb1+":")
            for each in hermesNames:
                name = hermesNames[count].split('//')  
                string = (string+"\n<a href=\"https://explorer.ambrosus.io/address/"+hermesAddress[count]+"\">"+name[1]+"</a>") 
                count = count + 1

        #open hermesTest buffer
        if hideTestnet != "1":
            f = open(home+folder+"hermesTest.txt","r")
            hermesTest = f.readlines()
            f.close()
            count = 0
            hermesTestList = []
            hermesTestAddressList = []
            switchHeadline = 0
            for each in hermesTest:
                hermesTest[count] = (hermesTest[count].replace("\n", ""))
                countherm = 0
                for info in hermesTestNames:
                    if hermesTest[count] == hermesTestNames[countherm]:
                        if hideHeartbeat == "1":
                            if hermesTest[count] == "https://hermes0.ambrosus-test.io/nodeinfo":
                                print("Ignoring Heartbeat Test-Hermes 0")
                            elif hermesTest[count] == "https://hermes1.ambrosus-test.io/nodeinfo":
                                print("Ignoring Heartbeat Test-Hermes 1")
                            elif hermesTest[count] == "test-nop.ambrosus-test.com":
                                print("Ignoring Nop-Test-Hermes")
                            #elif hermesTest[count] == "internal-test.ambrosus-test.io":
                            #    print("Ignoring Heartbeat Internal-Test-Hermes 2")
                            else:
                                counta = count + 1
                                diff = int(hermesTestBundles[countherm]) - int(hermesTest[counta])
                                if int(diff) > 0:
                                    if switchHeadline == 0:
                                        string = (string+"\n\nTEST-NET Hermes:")
                                        switchHeadline = 1
                                    celeb = ''
                                    if int(diff) >= 1 and int(diff) <= 4:
                                        celeb = '\U0001F331'
                                    elif int(diff) >= 5:    
                                        celeb = '\U0001F441'
                                    name = hermesTestNames[countherm].split('//')      
                                    string = (string+"\n<a href=\"https://explorer.ambrosus-test.io/address/"+hermesTestAddress[countherm]+"\">"+name[1]+"</a>\n"+"New Bundles: "+str(diff)+celeb)  
                        else:
                            counta = count + 1
                            diff = int(hermesTestBundles[countherm]) - int(hermesTest[counta])
                            if int(diff) > 0:
                                if switchHeadline == 0:
                                    string = (string+"\n\nTEST-NET Hermes:") 
                                    switchHeadline = 1
                                celeb = ''
                                if int(diff) >= 1 and int(diff) <= 4:
                                    celeb = '\U0001F331'
                                elif int(diff) >= 5:    
                                    celeb = '\U0001F441'
                                name = hermesTestNames[countherm].split('//')      
                                string = (string+"\n<a href=\"https://explorer.ambrosus-test.io/address/"+hermesTestAddress[countherm]+"\">"+name[1]+"</a>\n"+"New Bundles: "+str(diff)+celeb)
                    countherm = countherm + 1
                count = count + 1

        #overwrite hermesTest buffer
        f = open(home+folder+"hermesTest.txt","w")
        text = ""
        count = 0
        for each in hermesTestNames:
            if count == len(hermesTestNames)-1:
                text = (text + hermesTestNames[count]+"\n"+hermesTestBundles[count])
            else:
                text = (text + hermesTestNames[count]+"\n"+hermesTestBundles[count]+"\n")
            count = count + 1

        f.writelines(text)
        f.close()

        if hideTestnet != "1":
            count = 0
            for each in hermesTest:
                countherm = 0
                for info in hermesTestNames:
                    try:
                        if hermesTest[count] == hermesTestNames[countherm]:
                            hermesTestNames.pop(countherm)
                            hermesTestAddress.pop(countherm)
                    except IndexError:
                        print("")
                    countherm = countherm + 1
                count = count + 1

            if len(hermesTestNames) > 0:
                count = 0
                string = (string+"\n\nNew Test-Hermes"+celeb1+":")
                for each in hermesTestNames:
                    name = hermesTestNames[count].split('//')  
                    string = (string+"\n<a href=\"https://explorer.ambrosus-test.io/address/"+hermesTestAddress[count]+"\">"+name[1]+"</a>") 
                    count = count + 1

        if hermesinfo == "0":
            string = ""

#Send daily status message
        if statusmessage == "1":
            send_message(str(datewrite)+"\n\n"+str(atlasstring)+"\n"+str(apollostring)+"\nNetwork Stats:\nAtlasnodes = "+atlasnum+"\nApollonodes = "+apollonum+"\nHermesnodes = "+hermesnum+"\nAll Stake = "+str(int(AllStake))+" AMB\nTxns per Block = "+str(AverageBlockTransactions)+"\nDaily Usage = "+str(networkBundles)+" Bundles\nBundlecost = "+str(Bundlecost)+" AMB\nNext Month = "+str(nextcost)+" AMB\n"+str(payout)+"Price = "+str(price)+" "+str(currency)+str(string)+"\n\n--------------------------")

        if (len(atlasnodes)) > 0:
            statsfile = open(home+folder+"atlasbuffer.txt","w")
            statsat = statsfile.writelines(writeatlasbundlebuffer)
            statsfile.close()

        if (len(apollonodes)) > 0:    
            statsfile = open(home+folder+"apollobuffer.txt","w")
            statsap = statsfile.writelines(writeapollobalancebuffer)
            statsfile.close()


