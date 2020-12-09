#Enter your Settings here:
#------------------------------------------------------------

#enter your home directory with your username
home = "/home/myusername/"

#enter your Telegram Token and chat id
Telegram_Token = ''
Telegram_Chat_ID = ''

#enter your atlas node(s) in the brackets, seperated by comma and surrounded by inverted commas like this ['0x21...','0x35...','0x64...']
atlasnodes = []

#enter your apollo node(s) in the brackets, seperated by comma and surrounded by inverted commas like this ['0x21...','0x35...','0x64...']
apollonodes = []


#Send daily status message? (1 = yes, 0 = no)
statusmessage = "1"

#Set (server)time when to send daily stats message
statstime = "1505"


#to set Bundle Warnings, enter as many values as you'd like to be notified at, seperated by comma and surrounded by inverted commas like this ['100','200','1000']
dailybundlewarnings = ['60','100','200','300']

#once a daily-bundles value has triggered a warning, how much lower does the value need to go, until it can be triggered again?
#without this mechanism, notifications would be sent repeatedly, if you get too many Bundle Warnings, raise the following value:
sensitivity = "10"

#---------------------------------------------------------------


import requests
import random
import os.path
from time import gmtime, strftime

nodeOffline = '\U0001f6a8'
nodeOnline = '\u2705'
lowBalance = '\u26A0\uFE0F'
celeb1 = '\U0001F389'
celeb2 = '\U0001F973'
celeb3 = '\U0001F37E'

#get time
time = strftime("%H%M", gmtime())
datewrite = strftime("%Y-%m-%d", gmtime())

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

api_url_base = 'https://explorer-api.ambrosus.com/atlases'
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
    response = requests.get(api_url_base)
    data = str(response.json())
    found = (data.split(each))
    search = (len(found))
    while search == 1:
        next = (data.split('next'))
        if (len(next)) < 2:
            statusatlas.append("OFFLINE")
            break
        else:
            pageCloseEnd = (next[1].split(','))
            pageCloserEnd = (pageCloseEnd[0].split(': '))
            pageEnd = pageCloserEnd[1]
            pageEnd = (pageEnd.replace("'", ""))
            newlink = ("https://explorer-api.ambrosus.com/atlases?next="+pageEnd)
            response = requests.get(newlink)
            data = str(response.json())
            found = (data.split(each))
            search = (len(found))

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
        send_message(nodeOffline+" Your Atlas Node "+str(count+1)+" has just gone offline! <a href=\"https://explorer.ambrosus.com/atlas/"+each+"\">"+each+"</a>\n\n-------------------------------")
        #send_message('Your Atlas Node '+str(count+1)+' has just gone offline! https://explorer.ambrosus.com/atlas/'+each)
    if statusatlas[count] == "ONLINE" and statsat[count] == "0":
        send_message(nodeOnline+" Your Atlas Node "+str(count+1)+" is back online! <a href=\"https://explorer.ambrosus.com/atlas/"+each+"\">"+each+"</a>\n\n-------------------------------")
        #send_message('Your Atlas Node '+str(count+1)+' is back online! <a href="https://explorer.ambrosus.com/atlas/'+each+">"+each+"</a>)
    if feebalance <= 10:
        print('Atlas balance is low: '+str(feebalance)) 
        send_message(lowBalance+" Your Atlas Node "+str(count+1)+" has a very low balance of "+ str(feebalance)+" AMB.\n\nFunds might soon not be sufficient to pay the nodes challenge transactions.\nPlease raise the balance: <a href=\"https://explorer.ambrosus.com/atlas/"+each+"\">"+each+"</a>\n\n-------------------------------")
    if statusatlas[count] == "ONLINE":
        Sat.append("1")
        iconatlas.append(nodeOnline)
    else:
        Sat.append("0")            
        iconatlas.append(nodeOffline)
    writeatlasbuffer.append(Sat[count]+"\n",)
    count = count + 1


#get apollo status
    
api_url_base = 'https://explorer-api.ambrosus.com/apollos'
count = 0
stateapollo = []
statusapollo = []
balanceapollo = []
Sap = []
writeapollobalancebuffer = []
iconapollo = []
for each in apollonodes:
    print("Apollo "+each)
    response = requests.get(api_url_base)
    data = str(response.json())
    found = (data.split(each))
    search = (len(found))
    while search == 1:
        next = (data.split('next'))
        if (len(next)) < 2:
            statusapollo.append("OFFLINE")
            break
        else:
            pageCloseEnd = (next[1].split(','))
            pageCloserEnd = (pageCloseEnd[0].split(': '))
            pageEnd = pageCloserEnd[1]
            pageEnd = (pageEnd.replace("'", ""))
            newlink = ("https://explorer-api.ambrosus.com/apollos?next="+pageEnd)
            response = requests.get(newlink)
            data = str(response.json())
            found = (data.split(each))
            search = (len(found))

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
        send_message(nodeOffline+" Your Apollo Node "+str(count+1)+" has just gone offline! <a href=\"https://explorer.ambrosus.com/atlas/"+each+"\">"+each+"</a>\n\n-------------------------------")
        #send_message('Your Apollo Node '+str(count+1)+' has just gone offline! https://explorer.ambrosus.com/apollo/'+each)
    if statusapollo[count] == "ONLINE" and statsap[count] == "0":
        send_message(nodeOnline+" Your Apollo Node "+str(count+1)+" is back online! <a href=\"https://explorer.ambrosus.com/atlas/"+each+"\">"+each+"</a>\n\n-------------------------------")
        #send_message('Your Apollo Node '+str(count+1)+' is back online! https://explorer.ambrosus.com/apollo/'+each)
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

print(reset)
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
api_url_info = 'https://explorer-api.ambrosus.com/info'
response = requests.get(api_url_info)
data = str(response.json())
closeBundles = (data.split(','))
closerBundles = (closeBundles[34].split(':'))
networkBundles = (closerBundles[1].replace(" ", ""))

closerBlockTransactions = (closeBundles[31].split(':'))
AverageBlockTransactions = (closerBlockTransactions[1].replace(" ", ""))

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
                apollostring = (apollostring+"<a href=\"https://explorer.ambrosus.com/apollo/"+str(apollonodes[count])+"\">Apollo "+str(count+1)+"</a>  "+str(iconapollo[count])+"\t "+str(int(float(balanceapollo[count])))+"\t new: "+str(int(float(baldifapollo[count])))+" AMB\n")
                count = count + 1
            apollostring = (apollostring+"                      –––––––––––––––––––\n                      "+str(int(balanceall))+" new: "+str(int(baldifallapollo))+" AMB\n")
            
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
                atlasstring = (atlasstring+"<a href=\"https://explorer.ambrosus.com/atlas/"+str(atlasnodes[count])+"\">Atlas "+str(count+1)+"</a>  "+str(iconatlas[count])+"\t "+str(int(float(bundlesatlas[count])))+"\tnew: "+str(int(float(baldifatlas[count])))+" Bundles\n")
                count = count + 1
            atlasstring = (atlasstring+"                     –––––––––––––––––––\n                     "+str(bundleall)+" new: "+str(baldifallatlas)+" Bundles\n")
        
        if statusmessage == "1":
            send_message(str(datewrite)+"\n\n"+str(atlasstring)+"\n"+str(apollostring)+"\nNetwork Stats:\nAtlasnodes = "+atlasnum+"\nApollonodes = "+apollonum+"\nHermesnodes = "+hermesnum+"\nAll Stake = "+str(int(AllStake))+" AMB\nTxns per Block = "+str(AverageBlockTransactions)+"\nDaily Usage = "+str(networkBundles)+" Bundles\nBundlecost = "+str(Bundlecost)+" AMB\n\n--------------------------")

        if (len(atlasnodes)) > 0:
            statsfile = open(home+folder+"atlasbuffer.txt","w")
            statsat = statsfile.writelines(writeatlasbundlebuffer)
            statsfile.close()

        if (len(apollonodes)) > 0:    
            statsfile = open(home+folder+"apollobuffer.txt","w")
            statsap = statsfile.writelines(writeapollobalancebuffer)
            statsfile.close()
