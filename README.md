# Get_forecast_from_terminal
The script makes short links using API of [bit.ly](https://bit.ly) and writes it in terminal by user's query or counts total clicks on short links by user's query.

# How to start

Python3 should be already installed. Then use pip (or pip3, if there is a conflict with Python2) to install dependencies:

```bash
pip install -r requirements.txt
```
Before running a programm you need to make a .env file in the same directory with your script.

It's recommended to use virtual environment to isolate projects files, libraries and modules.

In this file you need to put your access token (variable `BITLY_TOKEN`) for API of [bit.ly](https://bit.ly) (first - you will make an account on [bit.ly](https://bit.ly), second - you will generate an access token on [app.bitly.com/settings/api/](https://app.bitly.com/settings/api/)). 

### Run

usage: main.py [-h] url

positional arguments:
  url         Your URL or bitlink

optional arguments:
  -h, --help  show this help message and exit
  
Launch on Linux or Windows as simple

```bash
$ python main.py https://sports.ru

# You will see

$ python main.py https://sports.ru
Битлинк: https://bit.ly/3B39pze
$ python main.py https://bit.ly/3B39pze
По вашей ссылке прошли: 1 раз(а)

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
