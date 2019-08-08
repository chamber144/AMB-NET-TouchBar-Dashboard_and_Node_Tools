# AMB-NET-Touchbar-Dashboard

![alt text](https://github.com/inlak16/AMB-NET-Touchbar-Dashboard/blob/master/tutorial-images/Node_Control_Touchbar_sm_.jpg)
![alt text](https://github.com/inlak16/AMB-NET-Touchbar-Dashboard/blob/master/tutorial-images/Node_Info_Touchbar_.jpg)

Hello fellow AMB-Net node operators. Welcome to this little repository.

Here I present a complete setup that may help you monitor and control your ATLAS or APOLLO through a MacBook Touchbar.

Please note that this is NOT an official tool created by Ambrosus, but a set that I built to control my own node and found quite useful to share with the whole community. 
Although I don't expect any dangerous errors to occur, I give no warranty that this is bug-free, so please look at the code, before running it. 

Also note that as soon as the Ambrosus-API is altered in any way, the pulled node info might not work as expected anymore and changes to the code may be needed. Thats why I'm posting all the code snippets in here seperately aswell.
_These code snippets can be encapsulated as executable apple scripts with Automator, too. So they may be helpful even without a Touch bar._
There may be a much better way to pull node information like sheltered bundles for Atlas in the future. 
Right now the scripts are iterating through many pages of transactions to count an atlas nodes challenges, which takes a few seconds to load for the first time.


### Installing BetterTouchTool

So let's get started. My setup only works with a tool called BetterTouchTool, which you can purchase for around 7 USD for a 2 year license or try for free for 45 days:

https://folivora.ai/buy

https://bettertouchtool.net/releases/BetterTouchTool.zip

If you ask yourself if this is worth it, I definitely say, yes. The devs regularly update the software and compared to other mac tools, 7 bucks is not too expensive.
Luckily this is the only thing that needs to be bought if you already own a MacBook with Touch bar. Quite some time I have wondered if it was really worth to get the more expensive MacBook with Touchbar. But now it has gotten really useful for quickly controlling my node on AMB-Net.


### Overview of BetterTouchTool and Dashboard

After you have purchased your BetterTouchTool license and installed the software, 
just open it and import the newest AMB-DASHBOARD*.bbtpreset file that I have put up here for download by using the preset function in the top right corner and click on import.

![alt text](https://github.com/inlak16/AMB-NET-Touchbar-Dashboard/blob/master/tutorial-images/01.png)


When the file has been loaded it should look something like this:

![alt text](https://github.com/inlak16/AMB-NET-Touchbar-Dashboard/blob/master/tutorial-images/02.png)



On the very left you have the programs that have touchbar presets in them. Closer to the center is the area where so called triggers are layered. These are individual setups that contain code snippets and are fully customizable, in the end being the single building blocks of the dashboard. If you click on one of them, you see on the right hand side that the containing parameters are shown. One of the most important is the enabled/visibility parameter to turn on and off single building blocks of the setup.



![alt text](https://github.com/inlak16/AMB-NET-Touchbar-Dashboard/blob/master/tutorial-images/03.png)



As you can see, I tried to keep it as flexible as possible. from top to bottom there is a **login script** (opening terminal with ssh connection), **a group of several login scripts** (In case you plan to run several nodes now that the floodgates to onboarding are open :D ), **two price tickers** (the first in EUR, which needs coinmarketcap api registration and the second in USD, running directly from Ambrosus API), **Apollo Online Status** (Online/Offline/Retired), **Apollo Main Stats** (Balance, Block, Stake), **Atlas Online Status** (Onboarded/Offline), **Atlas Main Stats** (Balance,Sheltered Bundles,Stake) and **AMB-Net Stats** (Daily Bundles, AMB per Bundle).


![alt text](https://github.com/inlak16/AMB-NET-Touchbar-Dashboard/blob/master/tutorial-images/05.png)


To give a better overview, here are two setups with different triggers activated and its resulting Dashboard that is activated by holding **Shift Command** on the keyboard.

**AMB USD - Atlas Online Status - Atlas Main Stats - AMB-Net Stats**:
![alt text](https://github.com/inlak16/AMB-NET-Touchbar-Dashboard/blob/master/tutorial-images/08.png)

**AMB USD - Apollo Online Status - Apollo Main Stats - AMB-Net Stats**:
![alt text](https://github.com/inlak16/AMB-NET-Touchbar-Dashboard/blob/master/tutorial-images/09.png)



### Setting up your node in the Dashboard

The addresses set for demonstration purposes are just the longest running nodes I could find and are likely run by Ambrosus.
Now lets add your node in there.
Set visibility of layers according to your nodetype and click on the online status layer.
On the right side there is the option to switch between common, which is mainly UI settings and widget-specific, which contains the whole Applescript to load a nodes online status into the dashboard.
Just enter your nodes public address into the script und click save at the top when the option comes up.



![alt text](https://github.com/inlak16/AMB-NET-Touchbar-Dashboard/blob/master/tutorial-images/04.png)



After doing the same with the according Main Stats Layer, the **Shift Command** Dashboard already works.
Activating the Online-Status-Layer again, now click on the "run apple script" at the top center.
This triggers commands when pushing the area of the touchbar where the building block/layer is appearing.



![alt text](https://github.com/inlak16/AMB-NET-Touchbar-Dashboard/blob/master/tutorial-images/07.png)



If you add your nodes public address in here, holding **Shift Command** and pushing on the Online Status of your node on the Touchbar opens the Ambrosus Explorer with your nodes page in Brave. If you dont have the Brave browser installed, you can change the script to any other browser.

Pushing the price ticker on the touchbar opens Ambrosus Reddit, Ambrosus Twitter and Coinmarketcap.

Tapping the grey AMB-net Info part of the Dashboard on the Touch bar opens the main page of the Ambrosus-Explorer.


### Logging into your node and preparations of the control Dashboard

Now that we have the visuals going, lets get to the control Dashboard.
As mentioned in the beginning, the top layers in BetterTouchTool are for logging into one or multiple nodes. You gain access to the scripts again with the run apple script button. Just input your user@ip and save.

I recommend running from user instead of root and if you want to have maximum security, install 2FA on your node:
https://www.linuxbabe.com/ubuntu/two-factor-authentication-ssh-key-ubuntu-18-04

![alt text](https://github.com/inlak16/AMB-NET-Touchbar-Dashboard/blob/master/tutorial-images/10.png)

You can create a preset in terminal with a background image for your node. And if you run more than one node, the apple script would switch the background according to the node to give a better visual overview on where you are logged in. If you use the Exit scripts that are on every level of the control Dashboard, the Terminal preset is automatically reset to Basic. If you are not using this, you may have to create a preset in Terminal called Basic or alter all the exit scripts. I've uploaded a PSD Photoshop file and created some network graphics variations, so you can fully customize your node backdrop image with your Server location and public address. For those of you that have no option to ob
pen a Photoshop file, I have generated some variations of the Backdrop and uploaded them here as png images. All of these can be found in the Node-Backdrop folder.

Layer overview of the Photoshop file:
![alt text](https://github.com/inlak16/AMB-NET-Touchbar-Dashboard/blob/master/tutorial-images/15.png)

Terminal Profile Settings with preset "Amb1" having loaded a Backdrop image called "Amb_node_1.png":
![alt text](https://github.com/inlak16/AMB-NET-Touchbar-Dashboard/blob/master/tutorial-images/11.png)


When you are logged in through the >_ button on the touchbar, BetterTouchTool automatically switches to the Triggers for the Terminal application on your Touch bar. There are two options on the top level. Analysis and Node Control.
![alt text](https://github.com/inlak16/AMB-NET-Touchbar-Dashboard/blob/master/tutorial-images/14.png)

Tapping on Analysis on the Touch bar gives all kind of options. But set set things up, first you should run 

`docker ps`

in Terminal and depending on wether you are running ATLAS or APOLLO, you insert the resulting IDs in the logs scripts in BetterTouchTool.
For APOLLO there is only one ID that has to be put in the Parity Logs script. Click Terminal on the left in BetterTouchTool and then double click the Analysis group, go to Parity Logs 1h and click run apple script to access the script.

![alt text](https://github.com/inlak16/AMB-NET-Touchbar-Dashboard/blob/master/tutorial-images/12.png)

For Atlas there are several IDs that docker ps outputs.
Atlas worker is the ID für the Atlas Logs scripts and Parity is for the Parity Log script. The Atlas log shows challenges and Parity logs shows the Blockchain connection through its Peercount (should be higher than 15 in my experience) and Blockheight (if node is showing offline, compare the Blockheight with the Ambrosus Explorer and see if the node is still syncing).

To save the log commands for multiple nodes, you can use the hidden group of log scripts a level higher outside the Analysis Group in BetterTouchTool.

### Analysis functions on the control Dashboard

From left to right here are the scripts in the Analysis Group that you can scroll through on your Touch bar:
**Atlas Logs 1h - Parity Logs 1h - Sheltered Bundles - TimeServer - TempBannedIP - BruteForce Protection - Granted Logins - Failed Logins - SSH Connections - Parity Version**
![alt text](https://github.com/inlak16/AMB-NET-Touchbar-Dashboard/blob/master/tutorial-images/13.png)

Just disable unneeded functions by turning off their Triggers visibility in BetterTouchTool.

The **Sheltered Bundles** function gives ATLAS node operators certainty of the Bundles held on their nodes harddrive.
If you tap this on the Touch Bar, it outputs a text in Terminal with the number of sheltered Bundles in the very last line.

**TimeServer** returns the connection to different ntp timeservers and its delay. I have this installed to be sure, my node has the correct time. You can install ntp simply by running the following. The last line is the same as in this function to query connection to timeservers:

`sudo timedatectl set-ntp off
timedatectl status
sudo apt install ntp
ntpq -p`

**TempBannedIP** is a function that calls a list of ips that have been banned through the BruteForce Protection.
I'm using Fail2Ban to permit bots and hackers from bruteforcing into my node. You can install the software by following these steps:

`sudo apt-get install -y fail2ban
sudo systemctl start fail2ban
sudo systemctl enable fail2ban
awk '{ printf "# "; print; }' /etc/fail2ban/jail.conf | sudo tee /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local`

This installs fail2ban and copies the configuration file so that you can easily modify the settings to your needs.
After running the last line the nano texteditor should be opened with the configuration file jail.local.
Here you go down in the text, until you find the following 3 Parameters: Max retry, Findtime, Bantime.
Erase the # in front of every of those parameters + in front of the next DEFAULT several lines above to activate this whole settings block. Then enter maximum Login attempts as max retry, the time a user has to try these number of login attempts and the time an ip is banned for if these tresholds are crossed. Note that this rule applies for your login device aswell.
So if you set 5 retries and 5000m bantime and type your ssh passwork wrong 5 times, your computers ip is banned for 83 hours. After setting these variables quit nano with **control x** and save the file. No restart fail2ban and test its status by running:

`sudo systemctl restart fail2ban
sudo systemctl status fail2ban`

The status should be returned with a green text showing that the protection is active. Now the **TempBannedIP** function returns the content of the ban list that is generated by malicious login attempts. After a few days you should see soome ips there already. Every now and then the ban list is reset, so don't worry, if the ban amounts get smaller at some time. 

The **BruteForce Protection** function simply shows the status of the fail2ban Bruteforce protection and how long it has been running.

With the **Granted Logins** function yu can check, who logged into your vps successfully. Quit with **Q** .

**Failed Logins** of course returns the opposite. And it's quite astonishing how many bots must be out there to try on all kind of ips all day.

The function **SSH Connections** returns just the attemps that have been done with a ssh connection.

With **Parity Version** you can simply check which version of parity your node is running on to know if an update is needed.

And that's if for the analisys part.

The Node control part is pretty self explanatory.
From left to right you stop the node, update the node and or the system and start the node again.

![alt text](https://github.com/inlak16/AMB-NET-Touchbar-Dashboard/blob/master/tutorial-images/16.png)

And that's basically the functionality for now. I'm excited to hear about ideas and useful commands that can be implemented.
If you like this dashboard and its functionality, feel free to send me a tip in AMB or ETH to the following address:

