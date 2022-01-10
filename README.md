# Trakt-Discord RPC Helper
A simple python script that acts as the bridge between the two services, allowing you to display your watch status in Discord directly from your Trakt.tv profile

# Dependencies
This script relies on quite a few python libraries. As such, I **highly** recommend using a [python virtual environment](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/)

You can install the required packages with the command:
```pip3 install -r requirements.txt```

# Setup
There are a few small things that need to be configured before you can start using the script

1. Edit the ```credentials.py``` file to have the required API keys and other personalized information
    * [Trakt.tv](https://trakt.tv/oauth/applications/new)
    * [Discord](https://discord.com/developers/applications)
2. Upload the artwork to your Discord RPC art assets in the developer portal

# Running the script
Running the script is easy! Just type: ```python3 disakt.py``` in your terminal and you'll be all set. You can mess around with auto-start configurations on your system to enable the script to run automatically when your PC starts up.
