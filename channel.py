from credentials import key,bot_token,channel_id,verifierchat_id
from db import User,Product,Order
from telegram.ext import *
import telegram
from message_handler import hd
import os



print("Bot started...")

APP_NAME='https://pure-escarpment-54630.herokuapp.com/'

PORT = int(os.environ.get('PORT',8443))

bot = telegram.Bot(token=key)
def start_command(update,context):
    if bool(context.args) and update.message.chat_id==verifierchat_id:        
        product = Product()
        # pdb.set_trace()
        id = int(context.args[0])
        arr=product.viewProds(id)
        response=''
        for i,prod in enumerate(arr):
            product.verify(prod[11])
            response+=f'''  
{i+1}. {prod[0]} {prod[2]}
{prod[1]}
Brand _ {prod[3]}
Country_ {prod[4]} 
Price _ {prod[5]}
Expiry date_ {prod[6]}
Stock amount _ {prod[8]}
Description _ {prod[7]}

'''
        bot.send_message(channel_id,response)
        return update.message.reply_text('The message has been posted to the channel')
    response='''This is upload bot where you can post your product
                And we will verify then post it on our channel.

                So we will need this information about your product

                Company name 
                Product name
                Product preparation 
                Product brand 
                Product country 
                Product price 
                Expiry date
                Description
                Stock amount
                for an example of how the post looks
                Amoxacilin syrup 250ml 

                Brand _ amoxil
                Country_ Germany
                Price _ 50bir per bottle 
                Expiry date _ September 2023
                Stock amount _ 100 cartoon 
                                              10 bottle per cartoon 
                Description _ immediate delivery
                                        Minimum 10 cartoon 
                                        Only cash, no credit 
'''

    update.message.reply_text(response)

    bot.send_message(update.message.chat_id,'To start tell us the name of your company?')


def exit_command(update,context):
    update.message.reply_text("exiting")
    print('exiting')


def error(update, context):
    print(f"Update {update} caused error {context.error}")
    
def handle_message(update,context):
    hd(update,context,bot,update.message.text,channel_id,verifierchat_id)

def main():
    updater = Updater(key)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler('exit',exit_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)
    # updater.start_polling()

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=key,
                          webhook_url=APP_NAME + key)
    updater.idle()


main()