import discord
from discord.ext import commands
import asyncio
import time
import random
import json
import os

# Dependant Variables #

TOKEN = 'NTM4MjcxNjcyNzQ3Mjk0NzIy.DyyOVA.ter8MjUmyo-sTn2JWEBtvvgZdew'

client = commands.Bot(command_prefix = "e!")
os.chdir(r'C:\Users\PC\OneDrive\DisConomyBOT')

helpembed = discord.Embed(
	title = "**DisConomy** Bot Commands",
	description = '''Prefix **e!**
		
		   ***GENERAL***
		**e!cmds** Shows a list of commands to the user
		**e!ping** Pings the bot
		**e!version** Shows the bot Version
		**e!invite** Shows the bot invite link
		**e!clear <amount>** Clears messages (default 100)
		
		   ***ECONOMY***
		**e!balance** Shows your coins
		**e!pay <@user> <amount>** Pays coisn to a user
		
		   ***SHOP***
		**e!shop** Shows the items urrently in the shop
		**e!buy <item number>** Buy an item with its item number in the shop
		
		   ***TRADING***
		**e!trade <@user>** Send a trade request to a user
		**e!accept** Accept the current trade request you have recieved
		**e!additem <item_name> <amount>** Add items to the trade
		**e!removeitem <item_name> <amount>** Remove items from the trade
		**e!confirm** Confirm the trade
	''',
	colour = discord.Colour.blue()
)

# Bot Startup # 

@client.event
async def on_ready():
	print("DisConomy Bot Ready.")
	await client.change_presence(game=discord.Game(name=str(len(client.servers))+" Servers", type=3))

# Coin Distribution #

@client.event
async def on_message(message):	
	with open('userData.json', 'r') as f:
		users = json.load(f)
	
	await update_data(users, message.author)
	if random.randint(4,8) == 8:
		await add_coins(users, message.author, random.randint(1,2))
	
	if random.randint(9,10) == 10:
		pass
		#print('droppedcoins')
		#await drop_coins(random.randint(25,75), message, message.channel)
	
	with open('userData.json', 'w') as f:
		json.dump(users, f)
		
	await client.process_commands(message)

#async def drop_coins(coins, message, channel):
	#print('DE')
	#print(channel)
	#channel = discord.utils.get(message.server.text_channels, name=channel)

	#client.send_message(channel, ":moneybag: *Look!* | Someone just *dropped* **"+str(coins)+"** Coins! \n***Grab*** them with **e!grab**")
	
@client.event
async def on_member_join(member):
	with open('userData.json', 'r') as f:
		users = json.load(f)
		
	with open('itemData.json', 'r') as f:
		useritms = json.load(f)
		
	await update_data(users, member)
	await update_items(useritms, member)
		
	with open('userData.json', 'w') as f:
		json.dump(users, f)
		
	with open('itemData.json', 'w') as f:
		json.dump(useritms, f) 

async def update_items(useritms, user):
	if not user.id in useritms:
		useritms[user.id] = {}
		useritms[user.id]['items'] = {}
		
async def update_data(users, user):
	if not user.id in users:
		users[user.id] = {}
		users[user.id]['coins'] = 0
		
async def add_coins(users, user, coins):
	users[user.id]['coins'] += coins	

# Commands #

@client.command(pass_context=True)
async def cmds(ctx):
	message = ctx.message
	await client.send_message(message.author, embed=helpembed)
	await client.say("{}, A list of *Commands* were sent to your **DMS**".format(ctx.message.author.mention)) 
	
@client.command(pass_context=True)
async def ping(ctx):  
	await client.say(' :ping_pong: *Pong!*')
	
@client.command(pass_context=True)
async def version(ctx):
	await client.say('**DisConomy** is running on version ***1.0***')

@client.command(pass_context=True)
async def invite(ctx):
	await client.say('Here is the link to invite ***DisConomy*** to your server \n https://discordapp.com/oauth2/authorize?client_id=538271672747294722&scope=bot&permissions=268561473')
	
@client.command(pass_context=True)
async def server(ctx):
	await client.say('Official **DisConomy** Server *Link*: \n   https://discord.gg/v2mhBqP')

@client.command(pass_context=True)
async def itemlist(ctx):
	embed = discord.Embed(
		title = "DisConomy Item List",
		description = "Here you can find what pages show what items",
		colour = discord.Colour.blue()
	)
	embed.add_author(name=' ', icon_url=client.user.default_avatar_url)

@client.command(pass_context=True)
async def clear(ctx, amount=100):
	channel = ctx.message.channel
	messages = []
	async for message in client.logs_from(channel, limit=int(amount)):
		messages.append(message)
	await client.delete_messages(messages)
	await client.say('Messaged *Deleted.*')
	
@client.command(pass_context=True)
async def balance(ctx):
	with open('userData.json', 'r') as f:
		users = json.load(f)
	await client.say(ctx.message.author.mention+', Your current balance is **'+str(users[ctx.message.author.id]['coins'])+'** coins.')

@client.command(pass_context=True)
async def pay(ctx, mention, amount):
	if mention is not None and amount is not None:
		if len(ctx.message.mentions) == 1:
			with open('userData.json', 'r') as f:
				users = json.load(f)
			
			if int(users[ctx.message.author.id]['coins']) >= int(amount) and int(amount) > 0:
				users[ctx.message.author.id]['coins'] -= int(amount)
				users[ctx.message.mentions[0].id]['coins'] += int(amount)
				print("Paying "+ctx.message.mentions[0].mention+str(amount))

				with open('userData.json', 'w') as f:
					json.dump(users, f)

@client.command(pass_context=True)
async def shop(ctx):
	with open('itemShop.json', 'r') as f:
		items = json.load(f)
	
	desc = " "
	i = 0
	while i < len(items):
		desc = desc+str(i+1)+" | :"+items[str(i)]['name']+": **"+items[str(i)]['name']+"** | ***Price***: "+str(items[str(i)]['price'])+" | Items Left: "+str(items[str(i)]['count'])+" \n "
		i += 1
		
	shopembed = discord.Embed(
		title = "DisConomy Shop",
		description = desc,
		colour = discord.Colour.blue()
	)
	await client.send_message(ctx.message.channel, embed=shopembed)
		
@client.command(pass_context=True)
async def buy(ctx, item):
	item = str(int(item)-1)
	
	with open('itemShop.json', 'r') as f:
		items = json.load(f)
		
	with open('userData.json', 'r') as f:
		users = json.load(f)
	
	print('debug')
	if items[item] != None:
		print('debug')
		with open('itemData.json', 'r') as f:
			useritms = json.load(f)
		
		if items[item] != None:
			print('debug')
			if items[item]['count'] > 0:
				if users[ctx.message.author.id]['coins'] >= items[item]['price']:
					users[ctx.message.author.id]['coins'] -= items[item]['price']
					print('debug')
				
					i = 0
					hadalready = False
					for it in useritms[ctx.message.author.id]['items']:
						if len(useritms[ctx.message.author.id]['items']) > 0:
							if useritms[ctx.message.author.id]['items'][it]['name'] == items[item]['name']:
								print('debug')
								useritms[ctx.message.author.id]['items'][it]['count'] += 1
								items[item]['count'] -= 1
								hadalready = True
								await client.say(ctx.message.author.mention+", You Successfully purchased 1 :"+items[item]['name']+": **"+items[item]['name']+"**!")
								break
							i += 1
					
					if hadalready == False:
						print('debug')
						num = len(useritms[ctx.message.author.id]['items'])
						useritms[ctx.message.author.id]['items'][num] = {}
						useritms[ctx.message.author.id]['items'][num]['name'] = items[item]['name']
						useritms[ctx.message.author.id]['items'][num]['count'] = 1
						items[item]['count'] -= 1
						await client.say(ctx.message.author.mention+", You Successfully purchased 1 :"+items[item]['name']+": **"+items[item]['name']+"**!")
			else:
				await client.say("Sorry, "+ctx.message.author.mention+"! We're all out of :"+items[item]['name']+": **"+items[item]['name']+"(s)**!")
	
	with open('userData.json', 'w') as f:
		json.dump(users, f)
	
	with open('itemData.json', 'w') as f:
		json.dump(useritms, f)
		
	with open('itemShop.json', 'w') as f:
		json.dump(items, f)
		
@client.command(pass_context=True)
async def trade(ctx, user):
	if user != None: #Make sure there is a first argument
		if len(ctx.message.mentions) == 1: #Make sure there was a user mentioned
			with open('tradeHandle.json', 'r') as f:
				trade = json.load(f)
			
			inTrade = False
			for trad in trade['trades']: #Check to see if the sender & recivers are not in trades
				if trade['trades'][trad]['a']['id'] == str(ctx.message.author.id) or trade['trades'][trad]['b']['id'] == str(ctx.message.author.id):
					inTrade = True
				if trade['trades'][trad]['a']['id'] == str(ctx.message.mentions[0].mention) or trade['trades'][trad]['b']['id'] == str(ctx.message.mentions[0].mention):
					inTrade = True
		
			if inTrade == True: #If they are in a trade, let them know
				await client.say("Sorry, "+ctx.message.mentions[0].mention+" or **you** are already in a trade.")
			else: # Or if they arent
				if not ctx.message.mentions[0].id == ctx.message.author.id:
					if not ctx.message.mentions[0].id in trade['tradeRequests']: #Check to see if the mentioned user is not registered in the requests json
						trade['tradeRequests'][ctx.message.mentions[0].id] = {} #If not, adds them to the json and sets their request to be from the sender
						trade['tradeRequests'][ctx.message.mentions[0].id]['sender'] = ctx.message.author.id
						trade['tradeRequests'][ctx.message.mentions[0].id]['reciever'] = ctx.message.mentions[0].id
						trade['tradeRequests'][ctx.message.mentions[0].id]['time'] = time.time()
					await client.say("Successfully sent a ***Trade Request*** to "+ctx.message.mentions[0].mention+"!")
					await client.send_message(ctx.message.mentions[0], ctx.message.mentions[0].mention+", You recieved a ***Trade Request*** from "+ctx.message.author.mention+"! \n   **Accept** the request with **e!accept**")
					with open('tradeHandle.json', 'w') as f:
						json.dump(trade, f)
				else:
					await client.say(ctx.message.author.mention+", Nice try! You cant send a ***Trade Request***  to *Yourself!*")
					
@client.command(pass_context=True)
async def accept(ctx):
	with open('tradeHandle.json', 'r') as f:
		trade = json.load(f)
	if ctx.message.author.id in trade['tradeRequests']:
		if trade['tradeRequests'][ctx.message.author.id] != 0 and trade['tradeRequests'][ctx.message.author.id] != "0" and trade['tradeRequests'][ctx.message.author.id] != " " and trade['tradeRequests'][ctx.message.author.id] != "":
			if int(trade['tradeRequests'][ctx.message.author.id]['time']) <= int(time.time()+300):
				trading = False
				for tr in trade['trades']:
					if trade['trades'][tr]['a']['id'] == ctx.message.author.id or trade['trades'][tr]['b']['id'] == ctx.message.author.id:
						trading = True
				if trading == False:
					leng = len(trade['trades'])
					trade['trades'][leng] = {}
					trade['trades'][leng]['a'] = {}
					trade['trades'][leng]['a']['id'] = ctx.message.author.id
					trade['trades'][leng]['a']['items'] = {}
					trade['trades'][leng]['a']['confirm'] = False
					trade['trades'][leng]['b'] = {}
					trade['trades'][leng]['b']['id'] = trade['tradeRequests'][ctx.message.author.id]["sender"]
					trade['trades'][leng]['b']['items'] = {}
					trade['trades'][leng]['b']['confirm'] = False
					tradembed = discord.Embed(
						title = "Item Trade",
						description = '''This is an Item Trade between '''+ctx.message.author.mention+''' and <@'''+trade['tradeRequests'][ctx.message.author.id]["sender"]+'''> 
							**'''+ctx.message.author.mention+'''**'s Items
							```                                        ```
							**<@'''+trade['tradeRequests'][ctx.message.author.id]["sender"]+'''>**'s Items
							```                                        ```
							cancel the trade with *e!cancel*
						''',
						colour = discord.Colour.blue()
					)
					msg = await client.say("the ***Trade Request*** was accepted. \n Add an item with **e!additem <item_name> <amount>** ", embed=tradembed)
					trade['trades'][leng]['message'] = msg.id
					trade['trades'][leng]['channel'] = ctx.message.channel.id
					del trade['tradeRequests'][ctx.message.author.id]
					with open('tradeHandle.json', 'w') as f:
						json.dump(trade, f)
				else:
					await client.say("Sorry, *you* are already in a  ***Trade***")
			else:
				await client.say("Sorry, the ***Trade Request*** has expired.")
				
@client.command(pass_context=True)
async def cancel(ctx):
	with open('tradeHandle.json', 'r') as f:
		trade = json.load(f)
	
	trading = None	
	for trad in trade['trades']:
		if trade['trades'][trad]['a']['id'] == str(ctx.message.author.id) or trade['trades'][trad]['b']['id'] == str(ctx.message.author.id):
			trading = trad
			break
	
	if trading != None:
		await client.send_message(ctx.message.server.get_member(trade['trades'][trad]['a']['id']), "<@"+trade['trades'][trad]['a']['id']+">, The trade with <@"+trade['trades'][trad]['b']['id']+"> been cancelled.")
		await client.send_message(ctx.message.server.get_member(trade['trades'][trad]['b']['id']), "<@"+trade['trades'][trad]['b']['id']+">, The trade with <@"+trade['trades'][trad]['a']['id']+"> been cancelled.")
		try:
			await client.http.delete_message(int(trade['trades'][trading]['channel']), int(trade['trades'][trading]['message']))
		except:
			await client.send_message(ctx.message.author, "TRADING ERROR | Error Number 002" )
		del trade['trades'][trading]
		
	with open('tradeHandle.json', 'w') as f:
		json.dump(trade, f)

@client.command(pass_context=True)
async def additem(ctx, item, amount):
	with open('tradeHandle.json', 'r') as f:
		trade = json.load(f)
	with open('itemData.json', 'r') as f:
		useritms = json.load(f)
	
	trading = None
	for trad in trade['trades']:
		if trade['trades'][trad]['a']['id'] == str(ctx.message.author.id) or trade['trades'][trad]['b']['id'] == str(ctx.message.author.id):
			trading = trad
			
	if trading != None:
		if item != None and amount != None:
			if str(ctx.message.author.id) in useritms:
				for itm in useritms[str(ctx.message.author.id)]['items']:
					if useritms[str(ctx.message.author.id)]['items'][itm]['name'] == item:
						if int(useritms[str(ctx.message.author.id)]['items'][itm]['count']) >= int(amount):
							print('Adding '+amount+' '+item+'(s)')
							print('debug '+trade['trades'][trad]['channel']+' '+trade['trades'][trad]['message']+' ')
							await client.http.delete_message(int(trade['trades'][trad]['channel']), int(trade['trades'][trad]['message']))
							if trade['trades'][trad]['a']['id'] == ctx.message.author.id:
								if item in trade['trades'][trad]['a']['items']:
									#Already some of that item in the trade
									theamt = amount
									if useritms[str(ctx.message.author.id)]['items'][itm]['count'] - trade['trades'][trad]['a']['items'][item]['count'] >= int(amount):
										trade['trades'][trad]['a']['items'][item]['count'] += int(amount)
								else:
									trade['trades'][trad]['a']['items'][item] = {}
									trade['trades'][trad]['a']['items'][item]['name'] = item
									trade['trades'][trad]['a']['items'][item]['count'] = int(amount)
							elif trade['trades'][trad]['b']['id'] == ctx.message.author.id:
								if item in trade['trades'][trad]['a']['items']:
									#Already some of that item in the trade
									if useritms[str(ctx.message.author.id)]['items'][itm]['count'] - trade['trades'][trad]['b']['items'][item]['count'] >= int(amount):
										trade['trades'][trad]['b']['items'][item]['count'] += int(amount)
								else:
									#None of that item were already in the trade
									trade['trades'][trad]['b']['items'][item] = {}
									trade['trades'][trad]['b']['items'][item]['name'] = item
									trade['trades'][trad]['b']['items'][item]['count'] = int(amount)
							else:
								client.send_message(ctx.message.author, 'TRADING ERROR   |  *Err Num* **001**')
							
							trade['trades'][trad]['a']['confirm'] = False
							trade['trades'][trad]['b']['confirm'] = False
							aitems = " "
							bitems = " "
							for it3m in trade['trades'][trad]['a']['items']:
								aitems = aitems+':'+str(trade['trades'][trad]['a']['items'][it3m]['name'])+': **'+trade['trades'][trad]['a']['items'][it3m]['name']+' x'+str(trade['trades'][trad]['a']['items'][it3m]['count'])+' |**'
							for it3m in trade['trades'][trad]['b']['items']:
								bitems = bitems+':'+str(trade['trades'][trad]['b']['items'][it3m]['name'])+': **'+trade['trades'][trad]['b']['items'][it3m]['name']+' x'+str(trade['trades'][trad]['b']['items'][it3m]['count'])+' |**'
							
							tradembed = discord.Embed(
								title = "Item Trade",
								description = '''This is an Item Trade between <@'''+trade['trades'][trad]['a']['id']+'''> and <@'''+trade['trades'][trad]['b']['id']+'''> 
									**<@'''+trade['trades'][trad]['a']['id']+'''>**'s Items   **|**
									**|**   '''+aitems+'''
									**<@'''+trade['trades'][trad]['b']['id']+'''>**'s Items   **|**
									**|**   '''+bitems+'''
									cancel the trade with *e!cancel*
								''',
								colour = discord.Colour.blue()
							)
							msg = await client.send_message(client.get_channel(trade['trades'][trad]['channel']), embed=tradembed)
							trade['trades'][trad]['message'] = msg.id
		
		with open('itemData.json', 'w') as f:
			json.dump(useritms, f)
		with open('tradeHandle.json', 'w') as f:
			json.dump(trade, f)

@client.command(pass_context=True)
async def removeitem(ctx, item, amount):
	if item != None and amount != None and amount:
		if int(amount) > 0:
			amount = int(amount)
			with open('tradeHandle.json', 'r') as f:
				trade = json.load(f)
			with open('itemData.json', 'r') as f:
				useritms = json.load(f)
			key = None
			trader = None
			all = None
			for trad in trade['trades']:
				if trade['trades'][trad]['a']['id'] == ctx.message.author.id:
					for itm in trade['trades'][trad]['a']['items']:
						if trade['trades'][trad]['a']['items'][itm]['name'] == item:
							if amount >= trade['trades'][trad]['a']['items'][itm]['count']:
								key = itm
								trader = 'a'
								all = True
								break
							else:
								trade['trades'][trad]['a']['items'][itm]['count'] -= amount
								key = itm
								trader = 'a'
								all = False
								break
				elif trade['trades'][trad]['b']['id'] == ctx.message.author.id:
					for itm in trade['trades'][trad]['b']['items']:
						if trade['trades'][trad]['b']['items'][itm]['name'] == item:
							if amount >= trade['trades'][trad]['b']['items'][itm]['count']:
								key = itm
								trader = 'b'
								all = True
								break
							else:
								trade['trades'][trad]['b']['items'][itm]['count'] -= amount
								key = itm
								trader = 'b'
								all = False
								break
			if key != None:
				print('Done Removal.')
				if all == True:
					del trade['trades'][trad][trader]['items'][key]
				
				trade['trades'][trad]['a']['confirm'] = False
				trade['trades'][trad]['b']['confirm'] = False
				aitems = " "
				bitems = " "
				for it3m in trade['trades'][trad]['a']['items']:
					aitems = aitems+':'+str(trade['trades'][trad]['a']['items'][it3m]['name'])+': **'+trade['trades'][trad]['a']['items'][it3m]['name']+' x'+str(trade['trades'][trad]['a']['items'][it3m]['count'])+' |**'
				for it3m in trade['trades'][trad]['b']['items']:
					bitems = bitems+':'+str(trade['trades'][trad]['b']['items'][it3m]['name'])+': **'+trade['trades'][trad]['b']['items'][it3m]['name']+' x'+str(trade['trades'][trad]['b']['items'][it3m]['count'])+' |**'
				
				tradembed = discord.Embed(
					title = "Item Trade",
					description = '''This is an Item Trade between <@'''+trade['trades'][trad]['a']['id']+'''> and <@'''+trade['trades'][trad]['b']['id']+'''> 
						**<@'''+trade['trades'][trad]['a']['id']+'''>**'s Items   **|**
						**|**   '''+aitems+'''
						**<@'''+trade['trades'][trad]['b']['id']+'''>**'s Items   **|**
						**|**   '''+bitems+'''
						cancel the trade with *e!cancel*
					''',
					colour = discord.Colour.blue()
				)
				await client.http.delete_message(int(trade['trades'][trad]['channel']), int(trade['trades'][trad]['message']))
				msg = await client.send_message(client.get_channel(trade['trades'][trad]['channel']), embed=tradembed)
				trade['trades'][trad]['message'] = msg.id
			else:
				client.say('Sorry '+ctx.message.author.id+', You cant do this right now.')
			
			with open('itemData.json', 'w') as f:
				json.dump(useritms, f)
			with open('tradeHandle.json', 'w') as f:
				json.dump(trade, f)
				
@client.command(pass_context=True)
async def confirm(ctx):
	with open('tradeHandle.json', 'r') as f:
		trade = json.load(f)
	with open('itemData.json', 'r') as f:
		useritms = json.load(f)
	
	re = False
	tra = None
	for trad in trade['trades']:
		if trade['trades'][trad]['a']['id'] == ctx.message.author.id:
			if trade['trades'][trad]['a']['confirm'] == False:
				trade['trades'][trad]['a']['confirm'] = True
				re = True
			else:
				await client.say(ctx.message.author.mention+", You are ***Already*** confirmed.")
			tra = trad
			break
		elif trade['trades'][trad]['b']['id'] == ctx.message.author.id:
			if trade['trades'][trad]['b']['confirm'] == False:
				trade['trades'][trad]['b']['confirm'] = True
				re = True
			else:
				await client.say(ctx.message.author.mention+", You are ***Already*** confirmed.")
			tra = trad
			break
	
	if re == True:
		aconf = ""
		bconf = ""
		if trade['trades'][trad]['a']['confirm'] == True:
			aconf = ':white_check_mark: ***CONFIRMED***'
		if trade['trades'][trad]['b']['confirm'] == True:
			bconf = ':white_check_mark: ***CONFIRMED***'
		aitems = " "
		bitems = " "
		for it3m in trade['trades'][trad]['a']['items']:
			aitems = aitems+':'+str(trade['trades'][trad]['a']['items'][it3m]['name'])+': **'+trade['trades'][trad]['a']['items'][it3m]['name']+' x'+str(trade['trades'][trad]['a']['items'][it3m]['count'])+' |**'
		for it3m in trade['trades'][trad]['b']['items']:
			bitems = bitems+':'+str(trade['trades'][trad]['b']['items'][it3m]['name'])+': **'+trade['trades'][trad]['b']['items'][it3m]['name']+' x'+str(trade['trades'][trad]['b']['items'][it3m]['count'])+' |**'
		
		tradembed = discord.Embed(
			title = "Item Trade",
			description = '''This is an Item Trade between <@'''+trade['trades'][trad]['a']['id']+'''> and <@'''+trade['trades'][trad]['b']['id']+'''> 
				**<@'''+trade['trades'][trad]['a']['id']+'''>**'s Items   **|**  '''+aconf+'''
				**|**   '''+aitems+'''
				**<@'''+trade['trades'][trad]['b']['id']+'''>**'s Items   **|**  '''+bconf+'''
				**|**   '''+bitems+'''
				cancel the trade with *e!cancel*
			''',
			colour = discord.Colour.blue()
			)
		await client.http.delete_message(int(trade['trades'][trad]['channel']), int(trade['trades'][trad]['message']))
		msg = await client.send_message(client.get_channel(trade['trades'][trad]['channel']), embed=tradembed)
		trade['trades'][trad]['message'] = msg.id
		
	if trade['trades'][trad]['a']['confirm'] == True and trade['trades'][trad]['b']['confirm'] == True:
		print('Trade Completed.')
		await client.say('Trade ***Complete!*** You will now recieve your items.')
		#Loop through the items that were in the trade for each player, and remove them from the player who added them and add them to the player recieving them
		
		for itm in trade['trades'][trad]['a']['items']:
			delet = []
			for i in useritms[trade['trades'][trad]['a']['id']]['items']:
				if useritms[trade['trades'][trad]['a']['id']]['items'][i]['name'] == itm:
					useritms[trade['trades'][trad]['a']['id']]['items'][i]['count'] -= trade['trades'][trad]['a']['items'][itm]['count']
					if useritms[trade['trades'][trad]['a']['id']]['items'][i]['count'] == 0:
						delet.append(i)
			if len(delet) > 0:
				for d in delet:
					del useritms[trade['trades'][trad]['a']['id']]['items'][d]
			added = False
			for i in useritms[trade['trades'][trad]['b']['id']]['items']:
				if useritms[trade['trades'][trad]['b']['id']]['items'][i]['name'] == itm:
					useritms[trade['trades'][trad]['b']['id']]['items'][i]['count'] += trade['trades'][trad]['a']['items'][itm]['count']
					added = True
			if added == False:
				l = len(useritms[trade['trades'][trad]['b']['id']]['items'])
				useritms[trade['trades'][trad]['b']['id']]['items'][l] = {}
				useritms[trade['trades'][trad]['b']['id']]['items'][l]['name'] = itm
				useritms[trade['trades'][trad]['b']['id']]['items'][l]['count'] = trade['trades'][trad]['a']['items'][itm]['count']
		for itm in trade['trades'][trad]['b']['items']:
			delet = []
			for i in useritms[trade['trades'][trad]['b']['id']]['items']:
				if useritms[trade['trades'][trad]['b']['id']]['items'][i]['name'] == itm:
					useritms[trade['trades'][trad]['b']['id']]['items'][i]['count'] -= trade['trades'][trad]['b']['items'][itm]['count']
					if useritms[trade['trades'][trad]['b']['id']]['items'][i]['count'] == 0:
						delet.append(i)
			if len(delet) > 0:
				for d in delet:
					del useritms[trade['trades'][trad]['b']['id']]['items'][d]
			added = False
			for i in useritms[trade['trades'][trad]['a']['id']]['items']:
				if useritms[trade['trades'][trad]['a']['id']]['items'][i]['name'] == itm:
					useritms[trade['trades'][trad]['a']['id']]['items'][i]['count'] += trade['trades'][trad]['b']['items'][itm]['count']
					added = True
			if added == False:
				l = len(useritms[trade['trades'][trad]['a']['id']]['items'])
				useritms[trade['trades'][trad]['a']['id']]['items'][l] = {}
				useritms[trade['trades'][trad]['a']['id']]['items'][l]['name'] = itm
				useritms[trade['trades'][trad]['a']['id']]['items'][l]['count'] = trade['trades'][trad]['b']['items'][itm]['count']
		
		del trade['trades'][trad]
	
	with open('itemData.json', 'w') as f:
		json.dump(useritms, f)
	with open('tradeHandle.json', 'w') as f:
		json.dump(trade, f)
	
	## Confirming a trade. Users will confirm, and a tick will show up next to their trade offer. If one user has confirms and either of them changes the trade, they will
	## automatically be unconfirmed. As soon as both users confirm, the trade will end and each user recieves their items.

@client.command(pass_context=True)
async def inventory(ctx):
	
	with open('itemData.json', 'r') as f:
		useritms = json.load(f)

	desc = " "
	int = 1
	for i in useritms[ctx.message.author.id]["items"]:
		desc = desc+str(int)+" | :"+useritms[ctx.message.author.id]["items"][i]['name']+": "+useritms[ctx.message.author.id]["items"][i]['name']+" | Count: "+str(useritms[ctx.message.author.id]["items"][i]['count'])+" \n "
		int+=1
		
	invembed = discord.Embed(
		title = ctx.message.author.name+"'s Inventory",
		description = desc,
		colour = discord.Colour.blue()
	)
	invembed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
	
	await client.send_message(ctx.message.channel, embed=invembed)
	
client.run(TOKEN)
