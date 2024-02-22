import telebot
import requests

API_TOKEN = '5707989635:AAE2pd-AN92KAZ_Gt1bL8LP0r7anE4ZO_NM'
URL = "https://dev-gpts.pantheonsite.io/wp-admin/js/apis/WormGPT.php"

bot = telebot.TeleBot(API_TOKEN)

# Define the user IDs of the admins
admins = [123456789, 987654321]

# Define a set to store premium members
premium_members = set()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "مرحبا بك في WormGPT .")

# Command to access the admin panel
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id in admins:
        bot.reply_to(message, "Welcome to the admin panel!\n"
                              "Use /addpremium @username to add a member to premium.\n"
                              "Use /kickpremium @username to kick a member from premium.")
    else:
        bot.reply_to(message, "Sorry, you are not authorized to access the admin panel.")

# Command to add a member to premium
@bot.message_handler(commands=['addpremium'])
def add_premium_member(message):
    if message.from_user.id in admins:
        if len(message.text.split()) != 2:
            bot.reply_to(message, "Usage: /addpremium @username")
            return
        username = message.text.split()[1]
        premium_members.add(username)
        bot.reply_to(message, f"{username} has been added to premium.")
    else:
        bot.reply_to(message, "Sorry, you are not authorized to add members to premium.")

# Command to kick a member from premium
@bot.message_handler(commands=['kickpremium'])
def kick_premium_member(message):
    if message.from_user.id in admins:
        if len(message.text.split()) != 2:
            bot.reply_to(message, "Usage: /kickpremium @username")
            return
        username = message.text.split()[1]
        if username in premium_members:
            premium_members.remove(username)
            bot.reply_to(message, f"{username} has been kicked from premium.")
        else:
            bot.reply_to(message, f"{username} is not a premium member.")
    else:
        bot.reply_to(message, "Sorry, you are not authorized to kick members from premium.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.from_user.username in premium_members:
        data = {
            "text": message.text,
            "api_key": "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",
            "temperature": 0.9
        }
        response = requests.post(URL, json=data).json()
        text = response["choices"][0]["message"]["content"]
        bot.reply_to(message, text, parse_mode='markdown')
    else:
        bot.reply_to(message, "Sorry, you need to be a premium member to use this bot.")

bot.polling(none_stop=True)
```

This code adds two new commands `/addpremium` and `/kickpremium` to the admin panel. Admins can use these commands to add or remove members to/from the premium list. The premium members can then access the bot's features, while non-premium members will receive a message indicating they need to upgrade to premium.
