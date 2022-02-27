from db import User,Product,Order
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import pdb

def hd(update,context,bot,text,channel_id,verifierchat_id):
	user = User()
	user.insert(update.message.chat_id,[])
	arr = user.find(update.message.chat_id)[1]
	if len(arr)==0:
		user.update(update.message.chat_id,[str(text)])
		update.message.reply_text('Now tell us the Product name?For example in the example it is "Amoxacilin"')

	elif len(arr)==1:
		arr.append(str(text))
		user.update(update.message.chat_id,arr)
		update.message.reply_text('Now tell us the Product preparation?For example in the example it is "syrup 250ml"')

	elif len(arr)==2:
		arr.append(str(text))
		user.update(update.message.chat_id,arr)
		update.message.reply_text('Now tell us the Product brand?For example in the example it is "amoxil"')
	
	elif len(arr)==3:
		arr.append(str(text))
		user.update(update.message.chat_id,arr)
		update.message.reply_text('Now tell us the Product country?For example in the example it is "Germany"')
	
	elif len(arr)==4:
		arr.append(str(text))
		user.update(update.message.chat_id,arr)
		update.message.reply_text('Now tell us the Product price?For example in the example it is "50bir per bottle"')
	
	elif len(arr)==5:
		arr.append(str(text))
		user.update(update.message.chat_id,arr)
		update.message.reply_text('Now tell us the Expiry date?For example in the example it is "September 2023"')
	
	elif len(arr)==6:
		arr.append(str(text))
		user.update(update.message.chat_id,arr)
		update.message.reply_text('''Now tell us the Description?For example in the example it is "immediate delivery Minimum 10 cartoon Only cash, no credit "''')

	elif len(arr)==7:
		arr.append(str(text))
		user.update(update.message.chat_id,arr)
		update.message.reply_text('Now tell us the Stock amount?For example in the example it is "100 cartoon 10 bottle per cartoon "')

	elif len(arr)==8:
		arr.append(str(text))
		user.update(update.message.chat_id,[])
		product = Product()
		id = product.insert(arr,update.message.chat_id)
		reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton(text='Post',url=f'https://telegram.me/tradeshopbot?start={id}')],
    ])
		bot.send_message(verifierchat_id,f'''
{arr[0]} {arr[2]}

Brand _ {arr[3]}
Country_ {arr[4]} 
Price _ {arr[5]}
Expiry date_ {arr[6]}
Stock amount _ {arr[8]}
Description _ {arr[7]}
''',reply_markup=reply_markup)
		update.message.reply_text('Great your is being verified now!')
		bot.send_message(update.message.chat_id,'Now tell us another one of your products and as such first please tell us your company name?')
