# Tracking daily Apollo Rewards automatically through a Python script 

As yearly Apollo reward transactions go into the hundredthousands, I wrote a little script that tracks rewards for up to 6 nodes on a daily basis.

Please note that _this is NOT an official tool created by Ambrosus_, but a setup that I built to track my own node during vacation and found quite useful to share with the whole community. 
Although I don't expect any dangerous errors to occur, _I give no warranty that this is bug-free_, so please have a look at the code, before running it. 

Also note that as soon as the AMB-Net API is altered in any way, the pulled node info might not work as expected anymore and changes to the code may be needed. Please get back to me on any edge cases you find. 


### Setting up the script

So let's get started. Log into your node and type (avoid using sudo for file access-reasons):

```
nano get_rewards_apollo.py
```

copy and paste the following script into the nano editor:

```
import requests
import os
import csv
from time import gmtime, strftime

os.system('ls')

#enter your home directory with you username
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
S = ["3","3","3","3","3","3","3"]
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
    balanceRealClose = (evenCloserBalance.split('.'))
    balance[count] = balanceRealClose[0]

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
    if status[count] == "ONLINE":
        S[count] = "1"
    else:
        S[count] = "0"
    print(status[count])
    count = count + 1


api_url_info = 'https://token.ambrosus.com/'
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
baldif0 = int(balance[0]) - int(buff[0])
if node2active == 1:
    buff[1] = (buff[1].replace("\n", ""))
    baldif1 = int(balance[1]) - int(buff[1])
if node3active == 1:
    buff[2] = (buff[2].replace("\n", ""))
    baldif2 = int(balance[2]) - int(buff[2])
if node4active == 1:
    buff[3] = (buff[3].replace("\n", ""))
    baldif3 = int(balance[3]) - int(buff[3])
if node5active == 1:
    buff[4] = (buff[4].replace("\n", ""))
    baldif4 = int(balance[4]) - int(buff[4])
if node6active == 1:
    buff[4] = (buff[5].replace("\n", ""))
    baldif5 = int(balance[5]) - int(buff[5])
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
    csv5 = ("\"Staking\",\""+str(baldif4)+"\",\"AMB\",\"\",\"\",\"\",\"\",\"\",\"\",\"Apollo Node6\",\""+datewrite+"\",\""+priceusd+"\"\n")
    csvfile.writelines(csv5)
csvfile.close()
```
At the top of the script adjust the username in the link according to your setup.
Input your Apollo Node Adress(es) and activate needed slots below the Adresses with the active-variables.

Be sure that in nano editor the very first text really is "import requests", otherwise the script will throw an error.

Exit nano and save the file with "control+X" confirming changes with "y".

Create another file typing (again its important to not use sudo):
```
nano buffer.txt
```

For every Apollo node you want to track type a 0 and press enter.
This is the buffer file that holds one value per line. It needs to be edited only the first time to contain the number of lines according to the number of nodes to track.

Exit nano and save the file with "control+x" confirming changes with "y".

You can test the script now by running:
```
python3 get_rewards_apollo.py
```

It should return the Nodeaddress and it's status ONLINE.
When there is no error shown, you can setup a cron job to automatically run the script once a day.
Type:

```
crontab -e
```
press 1 to use nano as standard editor for crontab
and enter the following line below the text:
```
0 22 * * * python3 /home/yourUserName/get_rewards_apollo.py
```
Change your username-directory accordingly as in the scriptfile before. 
"22" represents the hour the script is being executed. For this to happen at midnight in my timezone, I need to set it to 22.

Exit nano and save the file with "control+x" confirming changes with "y".

That's it. On the second day of execution this should result in a nice csv file even containing usd-AMB-price at the time of script execution.

Check the tracking anytime with this command:
```
nano rewards.csv
```
This data can be directly brought into Excel to make life easier.





If you like this project and find it useful, here is my Tip Jar that gratefully accepts AMB or ETH contributions:

_0xaBA817a774bf3dB1faB3c5cf867a82A683D74D22_

Please feel free to get back to me on Ambrosus slack. 
I'm planning to keep updating this repository the way I have time. 

[Here is a link to the over Updates to these scripts that have been done so far](https://github.com/inlak16/AMB-NET-TouchBar-Dashboard/blob/master/UPDATES)





