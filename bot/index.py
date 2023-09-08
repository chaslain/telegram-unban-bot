import telegram
import json
import os
from telegram.error import BadRequest

def lambda_handler(event, _context):

    debug = os.getenv("DEBUG_MODE") != None
    update = json.loads(event["body"])

    if debug:
        print(update)

    success_return = {"statusCode": "200"}

    block_user = os.getenv("UNAUTHORIZED_USER_ID")
    immune_user = os.getenv("IMMUNE_USER_ID")


    if immune_user == None:
        if debug:
            print('No immune user defined')

        return success_return

    if block_user == None:
        if debug:
            print('no block user defined')
        return success_return

    if debug:        
        print(update["chat_member"]["from"]["id"], block_user)
    
    block_users = set(block_user.split(','))
    immune_users = set(immune_user.split(','))

    if "chat_member" not in update:
        return success_return
        
    if str(update["chat_member"]["new_chat_member"]["status"]) not in ["kicked", "restricted"]:
        return success_return
    
    if str(update["chat_member"]["from"]["id"]) not in block_users:
        if debug:
            print('ban occured from non blocked user')
        return success_return
    
    if str(update["chat_member"]["new_chat_member"]["user"]["id"]) not in immune_users:
        if debug:
            print('ban occured to non immune user')
        return success_return
    
    bot = telegram.Bot(token=os.getenv("BOT_TOKEN"))


    try:
        if update["chat_member"]["new_chat_member"]["status"] == "restricted" \
        and update["chat_member"]["new_chat_member"]["can_send_messages"] == False:
            if debug:
                print("reverting mute")
            chat_permissions = telegram.ChatPermissions()
            chat_permissions.can_send_messages = True
            chat_permissions.can_send_media_messages = True
            result = bot.restrict_chat_member(update["chat_member"]["chat"]["id"], update["chat_member"]["new_chat_member"]["user"]["id"], chat_permissions)
            if debug:
                print("successfully reversed restriction" if result else "could not reverse restriction")
        
        if update["chat_member"]["new_chat_member"]["status"] == "kicked":
            if debug:
                print("reverting ban")
            result = bot.unban_chat_member(update["chat_member"]["chat"]["id"], update["chat_member"]["new_chat_member"]["user"]["id"])
        
            if debug:
                print("successfully reversed ban" if result else "could not reverse ban")
    except BadRequest as e:
        print(e)

    return success_return