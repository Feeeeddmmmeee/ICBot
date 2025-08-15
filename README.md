# ICBot
A Discord bot written in Python using Discord.py used in the official Intersection Controller server to view members' in-game user data.
## Installation
First clone the repository to your local machine and enter the freshly created folder.
```sh 
git clone https://github.com/Feeeeddmmmeee/ICBot
cd ICBot
```
Then set up all the required configuration files.
```sh
mkdir config
touch ./config/config.env
echo "TOKEN={YOUR_ACTUAL_TOKEN}" >> ./config/config.env
echo "DEBUG=1" >> .config/config.env
```
Lastly create a virtual environment, download all required packages and run the project :).
```sh
python3 -m venv env
source ./env/bin/activate
pip install -r requirements.txt
python3 main.py
```

## Configuration
All configuration is done in the `config/config.env` file. Not much can be configured without changing the source code as it was not needed at the time but below is a list of all the settings.
### Bot Token
The bot token has to be put in the `TOKEN` variable. 
### Debug Mode
Debug mode can be toggled by altering the `DEBUG` variable. Setting it to 1 enables additional log messages and changes which Discord server is considered the main one. 0 is supposed to be a release mode with less clutter in the logs and proper server settings.
