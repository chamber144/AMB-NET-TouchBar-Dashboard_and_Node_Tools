import requests
import random
from time import gmtime, strftime

#---------------------------------------------------------------

#enter your home directory with your username
home = '/home/myUserName/'


#enter your Telegram Token like this '1366402345:AA41ZAEV...' and chat id '514579...'
Telegram_Token = ''
Telegram_Chat_ID = ''


#enter your atlas node(s) in the brackets, seperated by comma and surrounded by inverted commas like this ['0x21...','0x35...','0x64...']
atlasnodes = []


#enter your apollo node(s) in the brackets, seperated by comma and surrounded by inverted commas like this ['0x21...','0x35...','0x64...']
apollonodes = []


#Send daily status message? (1 = yes, 0 = no)
statusmessage = '1'


#When to send daily stats message (Server time)?
statstime = '1505'


#---------------------------------------------------------------

nodeOffline = '\U0001f6a8'
nodeOnline = '\u2705'
lowBalance = '\u26A0\uFE0F'

#get time
time = strftime("%H%M", gmtime())
datewrite = strftime("%Y-%m-%d", gmtime())

#stats buffer file
if (len(atlasnodes)) > 0:
    statsfile = open(home+"statsatlas.txt","r")
    statsat = statsfile.readlines()
    statsfile.close()
    count = 0 
    for each in statsat:
        statsat[count] = (statsat[count].replace("\n", ""))
        count = count + 1

if (len(apollonodes)) > 0:
    statsfile = open(home+"statsapollo.txt","r")
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
            print("Atlas "+each+" is not synced yet. It needs to be synced and found in the API in order for the script to work properly")
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
    else:
        Sat.append("0")            
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
            print("Apollo "+each+" is not synced yet. It needs to be synced and found in the API in order for the script to work properly")
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
    else:
        Sap.append("0")
    writeapollobuffer.append(Sap[count]+"\n")        
    count = count + 1

#write statsbuffer
if (len(atlasnodes)) > 0:
    statsfile = open(home+"statsatlas.txt","w")
    statsat = statsfile.writelines(writeatlasbuffer)
    statsfile.close()

if (len(apollonodes)) > 0:    
    statsfile = open(home+"statsapollo.txt","w")
    statsap = statsfile.writelines(writeapollobuffer)
    statsfile.close()

#get general amb-net stats
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

#send daily stats
if time == statstime:
        baldifallapollo = 0
        baldifapollo = []
        apollostring = ""
        if (len(apollonodes)) > 0:
            bufffile = open(home+"apollobuffer.txt","r")
            count = 0
            buff = bufffile.readlines()
            bufffile.close()
            for each in buff:
                buff[count] = (buff[count].replace("\n", ""))
                baldifapollo.append(float(balanceapollo[count]) - float(buff[count]))
                baldifallapollo = baldifallapollo + baldifapollo[count]
                apollostring = (apollostring+"<a href=\"https://explorer.ambrosus.com/apollo/"+str(apollonodes[count])+"\">Apollo "+str(count+1)+"</a> "+str(statusapollo[count])+"\t "+str(int(float(balanceapollo[count])))+"\tnew: "+str(int(float(baldifapollo[count])))+" AMB\n")
                count = count + 1
            
        baldifallatlas = 0
        baldifatlas = []
        atlasstring = ""
        if (len(atlasnodes)) > 0:
            bufffile = open(home+"atlasbuffer.txt","r")
            count = 0
            buff = bufffile.readlines()
            bufffile.close()
            for each in buff:
                buff[count] = (buff[count].replace("\n", ""))
                baldifatlas.append(int(bundlesatlas[count]) - int(buff[count]))
                baldifallatlas = baldifallatlas + baldifatlas[count]
                atlasstring = (atlasstring+"<a href=\"https://explorer.ambrosus.com/atlas/"+str(atlasnodes[count])+"\">Atlas "+str(count+1)+"</a> "+str(stateatlas[count])+"\t "+str(int(float(bundlesatlas[count])))+"\tnew: "+str(int(float(baldifatlas[count])))+" Bundles\n")
                count = count + 1

        send_message(str(datewrite)+"\n\n"+str(atlasstring)+"\n"+str(apollostring)+"\nAMB-Net Atlas Stake = "+str(AtlasStake)+" AMB\nAMB-Net Apollo Stake = "+str(ApolloStake)+" AMB\nAll Stake = "+str(AllStake)+" AMB\n\nAverage Transactions per Block = "+str(AverageBlockTransactions)+"\nDaily Usage = "+str(networkBundles)+" Bundles\nBundlecost = "+str(Bundlecost)+" AMB\n\n--------------------------")

        #write bundle and balance buffer
        if (len(atlasnodes)) > 0:
            statsfile = open(home+"atlasbuffer.txt","w")
            statsat = statsfile.writelines(writeatlasbundlebuffer)
            statsfile.close()

        if (len(apollonodes)) > 0:    
            statsfile = open(home+"apollobuffer.txt","w")
            statsap = statsfile.writelines(writeapollobalancebuffer)
            statsfile.close()


