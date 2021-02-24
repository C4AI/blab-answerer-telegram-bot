# QAGeneratorBot
Telegram bot designed to easily distribute the work of creation of questions-answers pairs based on text spans of the Blue Amazon corpus.

It is important to fill in the ```'XXXXXX'``` on the 8th line in the ```QAGeneratorBot.py``` main file

```python
updater = Updater(token='XXXXXX', use_context=True)
```

with your own Telegram Token.

On your local/virtual machine, run the following commands in order to prepare the **environment** for the bot:
```
$ sudo apt update
$ sudo apt upgrade
$ sudo apt-get install software-properties-common
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt-get update
$ sudo apt-get install python3.6
$ sudo apt install python3-pip
$ python3.6 -m pip install telegram & python3.6 -m pip install python_telegram_bot
```

**Clone** the project from github:
```
$ git clone https://github.com/nakasato/blab-telegram-bot.git
$ cd blab-telegram-bot/
```

And, finally, put the bot to run in the **background**:
```
$ nohup python3.6 QAGeneratorBot.py &
```

To **check** whether the bot is running in the background:
```
$ ps -aux
```

To **kill** its related process:
```
$ kill pid XXXXX
```