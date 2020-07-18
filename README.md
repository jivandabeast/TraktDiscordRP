# Trakt-Discord RPC Helper
A simple python script that acts as the bridge between the two services, allowing you to display your watch status in Discord directly from your Trakt.tv profile

# Dependencies
This script relies on quite a few python libraries. As such, I **highly** recommend using a [python virtual environment] (https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/)
* Python 3
* urllib
* pypresence 
* dateutil.parser
* pytz
* time
* json

# Setup
There are a few small things that need to be configured before you can start using the script

1. Change the ```[username]``` on line 33 of ```disakt.py``` to display your Trakt.tv username
2. Edit the ```credentials.py``` file to have the required API keys
    * [Trakt.tv](https://trakt.tv/oauth/applications/new)
    * [Discord](https://discord.com/developers/applications)
3. Upload the artwork to your Discord RPC art assets in the developer portal

# Running the script
Running the script is easy! Just type: ```python3 disakt.py``` in your terminal and you'll be all set. (If you want to do something a little more resilient, you can mess around with autostarting the script in your operating system
