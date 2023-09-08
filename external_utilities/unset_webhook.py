import telegram

print("provide token")
token = input()
bot = telegram.Bot(token=token)



bot.delete_webhook(drop_pending_updates = True) and print("Successfully updated")
