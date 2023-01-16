# Telegram Bot for Online Flower Shop

Chat bot for Telegram application which helps customers to choose and buy items from online catalog and get professional consultations from florists based on their wishes. 


## How to start

First, you have to download this repository.

Python3 should be already installed. Then use pip (or pip3, if there is a conflict with Python2) to install dependencies:

```bash
pip install -r requirements.txt
```
Before running a programm you need to make a .env file in the same directory with your script.

It's recommended to use virtual environment to isolate projects files, libraries and modules.

In this file you need to put:
1) Access token (variable `TG_TOKEN`) for your telegram bot which you will use for the trade (first - you will make a new bot/or using your exisited in Telegram application with user - [https://t.me/BotFather](https://t.me/BotFather)).
2) Variable `FLORIST_ID` - Telegram ID of group or memeber (means that it will be a florist or florists) which will recieve messages from your trade-bot.
3) Variable `SERVICE_ID` - Telegram ID of group or memeber (means that it will be a person or persons who will deliver customer's orders) which will recieve messages from your trade-bot.
4) Variable `DEBUG` - for viewing information in case of mistake's appearances.
5) Variable `SECRET_KEY` - it's a secret key of the project (by default - "Admin Admin").

Second, you have to make superuser for working with database:

`python3 manage.py createsuperuser`

Third, you have to packaging up your model changes into individual migration files:

`python3 manage.py makemigrations`

Fourth, you have to apply these changes to your database:

`python3 manage.py migrate`

Fifth, you have to launch the server:

`python3 manage.py runserver`


## Run

There are two keyboard-commands in Telegram app. for operating with bot:

`/start` - Launch the bot.

`/cancel` - Stop the bot.


```diff
- After launching the bot you will see:
```


![Bot_step_1](https://user-images.githubusercontent.com/45304364/212697052-f748a255-651b-4682-ba14-112928a00651.png)


```diff
- Where you can choose the type of event for which you want to buy bouquet of flowers. 
- After choosing you will be asked about expecting price of the bouquet:
```


![Bot_step_2](https://user-images.githubusercontent.com/45304364/212699034-d6aa6452-ba95-462b-ab04-b4eaaa6b8d16.png)


```diff
- Then you can push `Заказать` for accepted offering from bot or continue to view another items or ask for callback from the florist.
```


![Bot_step_3](https://user-images.githubusercontent.com/45304364/212698804-54fdbbc1-a520-4ec4-9fad-ee2328da2508.png)


```diff
- Finally, you will be passed to approve the consent about personal's data processing.
- Then you should type your name, address, telephone number, date and time of delivery.
- Check the message from the bot with all information.
```

![Bot_step_4](https://user-images.githubusercontent.com/45304364/212701873-fdac1bb0-dfdd-4ca5-b1d4-f2e17232c920.png)

```diff
- Right after client's agreement with details of it's order, delivery service will recieve the message.
- This message will contain the details of order. And it will appear in their chat-group or a personal chat (if it is a one person).
- The same will happen with florist's group or florist-chat in case of leaving a phonenumber of the client.
```


![Bot_step_5](https://user-images.githubusercontent.com/45304364/212703130-04fb93cf-a606-4912-b499-d594e9e8ac47.png)


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
