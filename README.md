# ASVZ Bot - Automatic Enrollment Script


This is a simple ASVZ (Akademischer Sportverband Zürich) enrollment script for people who always miss the enrollment period of classes as cycling, rowing, etc. It is based on Python with Selenium. Currently, it only works with an ETH Zurich login, but it is quite easy to adapt it to other institutions (which I can't try since I don't have access).

Full instructions to set it up for automatic weekly enrollment are given below.

Works on the current version of the ASVZ website as of March 2019.

## Installation

These instructions are for Ubuntu. It was tested on Ubuntu 16.04, Python 3.5.2 and Firefox 65.0 with corresponding Geckodriver v0.24.0. Adapt to your own system if necessary.

Clone this repository:

```
cd
git clone https://github.com/jstiefel/asvz_bot.git
```

Set up new virtual environment with venv:

```
sudo pip install venv
python3 -m venv ~/asvz_bot_python
source asvz_bot_python/bin/activate
```

Install Selenium and Firefox webdriver:

```
pip install --upgrade pip
pip install selenium
cd Downloads
wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
tar -xvzf geckodriver*
chmod +x geckodriver
sudo mv geckodriver /usr/local/bin/
rm geckodriver-v0.24.0-linux64.tar.gz
deactivate
```

## Run

Enter your login credentials, the link to the corresponding "Sportfahrplan", day, time and facility on top in asvz_bot.py. Your data is safe since it just uses your own webbrowser. But only use it on your private device since credentials are saved in this file as plain text. 

There are two methods to use this script:

1. Run it manually on the day of enrollment
2. Run one or several as cron job on your device (e.g. Laptop, Raspberry Pi, ...) for automatic weekly enrollment

### 1. Run it manually

Run script once for single enrollment at defined time on the day before enrollment start. Don't close the terminal.

```
cd 
source asvz_bot_python/bin/activate
cd asvz_bot
python asvz_bot.py
```

### 2. Create a cron job

Copy asvz_bot.py for each enrollment you want to make in one week. Then define a cron job for each of these with corresponding time.

```
crontab -e
```

To run enrollment for example at 21:30 each Tuesday, enter:

```
30 21 * * 2 python asvz_bot.py
# Shell variable for cron
SHELL=/bin/bash
# PATH variable for cron
PATH=/usr/local/bin:/usr/local/sbin:/sbin:/usr/sbin:/bin:/usr/bin:/usr/bin/X11
# 
# m h  dom mon dow   command
30 21 * * 3 /home/<user>/asvz_bot_python/bin/python /home/<user>/asvz_bot/asvz_bot.py > /home/<user>/asvz_bot/asvz.log 2>&1
```

