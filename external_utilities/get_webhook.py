import telegram

print("provide token")
token = input()

bot = telegram.Bot(token=token)

print(bot.get_webhook_info())