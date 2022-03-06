from db import User,Product,Order,Products
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import pdb

def hd(update,context,bot,text,channel_id,verifierchat_id):
	user = User()
	user.insert(update.message.chat_id,[])
	arr = user.find(update.message.chat_id)[1]
	prods_id=user.viewOne(update.message.chat_id)[2]
	if len(arr)==0:
		user.update(update.message.chat_id,[str(text)],prods_id)
		update.message.reply_text('Product name?"')

	elif len(arr)==1:
		arr.append(str(text))
		user.update(update.message.chat_id,arr,prods_id)
		update.message.reply_text('Now tell us the Product preparation?For example in the example it is "syrup 250ml"')

	elif len(arr)==2:
		arr.append(str(text))
		user.update(update.message.chat_id,arr,prods_id)
		update.message.reply_text('Now tell us the Product brand?')
	
	elif len(arr)==3:
		arr.append(str(text))
		user.update(update.message.chat_id,arr,prods_id)
		update.message.reply_text('Now tell us the Product country?')
	
	elif len(arr)==4:
		arr.append(str(text))
		user.update(update.message.chat_id,arr,prods_id)
		update.message.reply_text('Now tell us the Product price?"')
	
	elif len(arr)==5:
		arr.append(str(text))
		user.update(update.message.chat_id,arr,prods_id)
		update.message.reply_text('Expiry date?')
	
	elif len(arr)==6:
		arr.append(str(text))
		user.update(update.message.chat_id,arr,prods_id)
		update.message.reply_text('''Now tell us the Description?For example in the example it is "immediate delivery Minimum 10 cartoon Only cash, no credit "''')

	elif len(arr)==7:
		arr.append(str(text))
		user.update(update.message.chat_id,arr,prods_id)
		update.message.reply_text('Now tell us the Stock amount?')

	elif len(arr)==8:
		# pdb.set_trace()
		arr.append(str(text))
		if not bool(user.viewOne(update.message.chat_id)[2]):
			products = Products()
			prods_id = products.insert([])
			user.update(update.message.chat_id,arr,prods_id)
			product = Product()
			id = product.insert(arr,update.message.chat_id,prods_id)
			products.update(prods_id,[id])
			keyboard = [['No','Yes']]
			reply_markup = ReplyKeyboardMarkup(keyboard,resize_keyboard=True)
			update.message.reply_text('Great your product is added do you want to add another one to your post?',reply_markup=reply_markup)	

		else :
			# pdb.set_trace()
			products = Products()
			prods_id=user.viewOne(update.message.chat_id)[2]
			user.update(update.message.chat_id,arr,prods_id)
			product = Product()
			id = product.insert(arr,update.message.chat_id,prods_id)
			pds_arr=products.viewOne(user.viewOne(update.message.chat_id)[2])[0]
			pds_arr.append(id)
			products.update(prods_id,pds_arr)
			keyboard = [['No','Yes']]
			reply_markup = ReplyKeyboardMarkup(keyboard,resize_keyboard=True)
			update.message.reply_text('Great your product is added do you want to add another one to your post?',reply_markup=reply_markup)	
		
	elif len(arr)==9:
		if text=='Yes':
			# pdb.set_trace()
			prods_id=user.viewOne(update.message.chat_id)[2]
			user.update(update.message.chat_id,arr[0:1],prods_id)
			reply_markup = ReplyKeyboardRemove()
			update.message.reply_text('Now tell us the Product name?',reply_markup=reply_markup)

		elif text=='No':
			prods_id=user.viewOne(update.message.chat_id)[2]
			product=Product()
			prods = product.viewProds(prods_id)
			response=''
			for i,prod in enumerate(prods):
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
		
			reply_markup=InlineKeyboardMarkup([
	        [InlineKeyboardButton(text='Post',url=f'https://telegram.me/tradeshopbot?start={prods_id}')],
	    ])
			bot.send_message(verifierchat_id,response,reply_markup=reply_markup)
			update.message.reply_text('Great your post is being verified now!',reply_markup = ReplyKeyboardRemove())
			bot.send_message(update.message.chat_id,'Now tell us another one of your products and as such first please tell us your company name?')
			user.update(update.message.chat_id,[])

		else :
			update.message.reply_text('I don\'t understand please use the buttons given')
