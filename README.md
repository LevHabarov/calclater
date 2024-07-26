<h1 align="center">calclater</h1>

<p align="center"><b>Calculator working via Telegram bot.</b></p>

## About

A python script that creates a simple calculator from an InlineKeyboardButton in Telegram, and using a SQLite database.

## How to use the script

Just enter the token in `config.py` and run `bot.py`

## Working Telegrab Bot:

https://t.me/CalcLaterBot

## Installation
```shell
# clone the repository
$ git clone https://github.com/LevHabarov/calclater.git

# change the working directory to calclater
$ cd calclater
```

## Configuring
**Open `config.py` configuration file with text editor and set the following variables:**
```ini
TG_BOT_TOKEN = '1234567890:AAA-AaA1aaa1AAaaAa1a1AAAAA-a1aa1-Aa'
```
* `TG_BOT_TOKEN` is token for your Telegram bot. You can get it here: [BotFather](https://t.me/BotFather).

## Running
### Using Python
```shell
# install requirements
$ python -m pip install -r requirements.txt

# run script
$ python bot.py
```

## License
GPLv3<br/>
Original Creator - [LevHabarov](https://github.com/LevHabarov)
