# AMB-NET-Touchbar-Dashboard

Hello fellow AMB-Net node operator. Welcome to this little repository.
Here I present a complete setup that may help you monitor and control your ATLAS or APOLLO through a MacBook Touchbar.

Please note that this is NOT an official tool created by Ambrosus, but a set that I built to control my own node and found quite useful to share with the whole community. 
Although I don't expect any dangerous errors, I give no warranty that this is bug-free, so please look at the code, before executing. 

Also note that as soon as the Ambrosus-API is altered in any way, the pulled node info might not work as expected anymore and changes to the code may be needed. Thats why I'm posting all the code snippets in here seperately aswell.

# Installing BetterTouchTool

So let's get started. My setup only works with a tool called BetterTouchTool, which you can purchase for 7,5 USD for a 2 year license or try for free for 45 days:

https://folivora.ai/buy

https://bettertouchtool.net/releases/BetterTouchTool.zip

If you ask yourself if it is worth it, I definitely say, yes. They regularly update the software and compared to other mac tools 7 bucks is not too expensive.
Luckily this is the only thing that needs to be bought if you are already own a MacBook with Touchbar. AQuite some time I have wondered if it was really worth to get the more expensive MacBook with Touchbar. But now it has gotten really useful for quickly controlling my node on AMB-Net.

# Getting Started

After you have purchased your BetterTouchTool license and installed the software, 
just open it and import the newest AMB-DASHBOARD*.bbtpreset file that I have put up here for download by using the preset function in the top right corner and click on import.

![alt text](https://github.com/inlak16/AMB-NET-Touchbar-Dashboard/blob/master/tutorial-images/01.png)

When the file has been loaded it should look something like this:

![alt text](https://github.com/inlak16/AMB-NET-Touchbar-Dashboard/blob/master/tutorial-images/02.png)

On the very left you have the programs that have touchbar presets in them. Closer to the center is the area where so called triggers are layered. These are individual setups that contain code snippets and are fully customizable, in the end being the single building blocks of the dashboard. If you click on one of them, you see on the right hand side that the containing parameters are shown. One of the most important is the enabled/visibility parameter to turn on and off single building blocks of the setup.

![alt text](https://github.com/inlak16/AMB-NET-Touchbar-Dashboard/blob/master/tutorial-images/03.png)

As you can see, I tried to keep it as flexible as possible. from top to bottom there is a **login script** (opening terminal with ssh connection), **a group of several login scripts** (In case you plan to run several nodes now that the floodgates to onboarding are open :D ), **two price tickers** (the first in EUR, which needs coinmarketcap api registration and the second in USD, running directly from Ambrosus API), **Apollo Online Status** (Online/Offline/Retired), **Apollo Main Stats** (Balance, Block, Stake), **Atlas Online Status** (Onboarded/Offline), **Atlas Main Stats** (Balance,Sheltered Bundles,Stake) and **AMB-Net Stats** (Daily Bundles, AMB per Bundle).

![alt text](https://github.com/inlak16/AMB-NET-Touchbar-Dashboard/blob/master/tutorial-images/05.png)

To give a better overview here are two setups with different triggers activated and its resulting Dashboard that is activated by holding **Shift Command**.

**AMB USD - Atlas Online Status - Atlas Main Stats - AMB-Net Stats**:
![alt text](https://github.com/inlak16/AMB-NET-Touchbar-Dashboard/blob/master/tutorial-images/08.png)

**AMB USD - Apollo Online Status - Apollo Main Stats - AMB-Net Stats**:
![alt text](https://github.com/inlak16/AMB-NET-Touchbar-Dashboard/blob/master/tutorial-images/09.png)
