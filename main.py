#Imports
import discord
import discord.utils
from discord.ext import commands
from discord.utils import get
import asyncio
import os
import json
import requests
import random

from PIL import Image
from io import BytesIO

#Commands Handler- DO NOT TOUCH
client = commands.Bot(command_prefix="-", case_insensitive = True)
member = discord.Member

#Removes the default help command. The Administrator has his own!
client.remove_command('help')


#Global Variables
vtriggers = "on"
#This means that the default setting for word triggers is "True"!

#Matrixes
filter = ['chemistry' , 'Chemistry']

eightballquestion = [":8ball:Ask again later" , ":8ball:For sure!" , ":8ball:Absolutely not." , ":8ball:Not sure yet." , ":8ball:Perhaps." , ":8ball:Absolutely!"]

rrmatrix = [f"'The body cannot live without the mind.' -Morpheus, The Matrix" , f"'Ever have that feeling where you’re not sure if you’re awake or dreaming?'' -Neo, The Matrix" , f"'I don’t like the idea that I’m not in control of my life.'' -Neo, The Matrix" , f"'Never tell me the odds!' - Han Solo, Star Wars", f"'It's time to spin the chamber, Boris.' -DeAngelo, The Office (US)", f"'Do not throw away your shot...' -Alexander Hamilton, Hamilton" , f"'Guns. Lots of guns.' -Neo, The Matrix"]

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name= str(len(client.guilds)) + " servers | -help"))
  print('Bot is ready!')

@client.event
async def on_message(message):
  if 'psychology' in message.content:
    await message.delete()
    await message.channel.send("Please do not say that. The staff have been notified.")
  
##TEMPORARY COMMANDS
@client.command()
async def standwithukraine(ctx , *, user: discord.Member):
  ukr = Image.open("ua.jpeg")
  asset = user.avatar_url_as(size = 128)
  data = BytesIO(await asset.read())
  ua1 = Image.open(data)
  ukr.paste(ua1, (230,160))
  ukr.save("uak1.jpeg")
  await ctx.send(file = discord.File("uak1.jpeg"))
  await ctx.send("Please also consider making a donation to support the people of Ukraine: https://bit.ly/3N35c2I")

@client.command()
@commands.has_permissions(manage_roles = True)
async def autorole(ctx, option = "N/A"):
  if option == "add":
    await ctx.send("Alright! What is the ID of the  channel would you like to add it to? [NOTE: You must have Developer Mode enabled to copy channel IDs.]")
    channel_role = await client.wait_for("message")
    channel_id = int(channel_role.content)
    channel = client.get_channel(channel_id)
    await ctx.send(f"Sending the autorole to **{channel}**.")
    await ctx.send("Great! Now, what is the name of the role you wish to add?")
    role_id_raw = await client.wait_for("message")
    role = discord.utils.get(ctx.guild.roles, name= str(role_id_raw.content))
    await ctx.send(f"Using **{role}** .")
    await ctx.send("What emote would you like to use?")
    emote = await client.wait_for("message")
    await ctx.send(f"Your selected emote is {emote.content}.")
    await ctx.send("What hex color would you like your embed to have?")
    hex = await client.wait_for("message")
    await ctx.send("And what is the title of your embed?")
    title_embed = await client.wait_for("message")
    await ctx.send("All set!")
    embed = discord.Embed(title = f"{title_embed.content}", description = f"{role}", color = str(hex.content)())
    await channel.send(embed=embed)
    
  
@client.command()
async def suggestionchannel(ctx, channel: discord.TextChannel):
  guild = ctx.guild
  with open("suggestion.json", "r") as f:
    suggest = json.load(f)
  await ctx.send(f"Success! Your suggestion channel has been set to {channel.mention}.")
  channel == channel.id
  if not f'{guild.id}' in suggest:
    suggest[f'{guild.id}'] = {}
    suggest[f'{guild.id}']['channel'] = "None"
  suggest[f'{guild.id}']['channel'] = f'{channel.id}'
  with open("suggestion.json" , "w") as f:
    suggest = json.dump(suggest, f)

@client.command()
async def suggest(ctx, * , suggestion = "N/A"):
  with open("suggestion.json", "r") as f:
    suggest = json.load(f)
  guild = ctx.guild
  chan = int(suggest[f'{guild.id}']['channel'])
  channel = client.get_channel(chan)
  if suggestion == "N/A":
    await ctx.send("Suggestion cannot be empty!")
    await asyncio.sleep(2)
  elif suggestion != "N/A":
    embed = discord.Embed(title = "Suggestion" , description = f"*Made by {ctx.author.name}*" , color = discord.Color.blue())
    embed.add_field(name = f"{suggestion}" , value = "\n\u200b", inline = True)
    await ctx.channel.purge(limit = 1)
    message = await channel.send(embed=embed)
    await message.add_reaction("✅")
    await message.add_reaction("❌")

@client.command()
async def feedbackchannel(ctx, channel: discord.TextChannel):
  guild = ctx.guild
  with open("feedback.json", "r") as f:
    feed = json.load(f)
  await ctx.send(f"Success! Your feedback channel has been set to {channel.mention}.")
  channel == channel.id
  if not f'{guild.id}' in feed:
    feed[f'{guild.id}'] = {}
    feed[f'{guild.id}']['channel'] = "None"
  feed[f'{guild.id}']['channel'] = f'{channel.id}'
  with open("feedback.json" , "w") as f:
    feed = json.dump(feed, f)

@client.command()
async def help(ctx, *, criteria = "Null"):
  if criteria == "Null":
    embed = discord.Embed(title="Help Page", description="The list of commands for The Administrator", color = discord.Color.red())
    embed.add_field(name = "**help emotes**" , value = "Shows the help menu for the bot's expanding emote list!" , inline = False)
    embed.add_field(name = "**help admin**" , value = "Shows the help menu for moderators and server staff!" , inline = False)
    embed.add_field(name = "**help fun**", value = "Shows the help menu for the fun commands, such as games and such!" , inline = False)
    embed.add_field(name = "**help economy**" , value = "Shows the help menu for the economy!" , inline = False)
    embed.add_field(name = "**invite**-" , value = "Sends an invite link so you can add The Administrator to your server!" , inline = False)
    embed.add_field(name = "**TEMPORARY COMMAND: standwithukraine [user]**-" , value = "Sends a picture with your avatar overlaid on the Ukraine flag." , inline = False)
    embed.set_thumbnail(url= ctx.author.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author.name}. Join the support server by typing -support!")
    await ctx.send(embed=embed)
  if criteria == "emotes":
    embed = discord.Embed(title = "**Emote Help Menu**" , description = "The Help Menu for Emotes!" , color = discord.Color.red())
    embed.add_field(name = "**Kiss [user]**-" , value = "Kisses the specified user" , inline = False)
    embed.add_field(name = "**hug [user]**-" , value = "Hugs the specified user" , inline = False)
    embed.add_field(name = "**boop [user]**-" , value = "Boops the specified user" , inline = False)
    embed.add_field(name = "**stare [user]**-" , value = "Stares at the specified user" , inline = False)
    embed.add_field(name = "**kill [user]**-" , value = "Kills the specified user" , inline = False)
    embed.set_footer(text = f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)
  if criteria == "admin":
    embed = discord.Embed(title = "**Administration Help Menu**" , description = "The Help Menu for Server Staff!" , color = discord.Color.red())
    embed.add_field(name = "**Grant [user] [role]**-" , value = "Grants selected user the role you specify." , inline = False)
    embed.add_field(name = "**Announce [message]**-" , value = "Sends an announcement in the current channel" , inline = False)
    embed.add_field(name = "**Accept [user] [role] [reason]**-" , value = "Sends a message in the current channel notifying others of your decision to promote them" , inline = False)
    embed.add_field(name = "**Deny [user] [role] [reason]**-" , value = "Sends a message in the current channel notifying others of your decision not to promote them" , inline = False)
    embed.add_field(name = "**Purge [amount]**-" , value = 'Purges selected amount of messages', inline = False)
    embed.add_field(name = "**Kick [user] [reason]**-" , value = 'Kicks the selected member and displays the reason' , inline = False)
    embed.add_field(name = "**Ban [user] [reason]**-" , value = "Bans the selected member and displays the reason" , inline = False)
    embed.add_field(name = "**unban [user+discriminator]**-" , value = "Unbans the selected member" , inline = False)
    embed.add_field(name = "**rules [input]**-" , value = "Embeds your server rules. Please note that there is a 1028 character limit per embed." , inline = False)
    embed.set_footer(text = f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)
  if criteria == "fun":
    embed = discord.Embed(title = "**Fun Help Menu**" , description = "The Help Menu for everything fun!!" , color = discord.Color.red())
    embed.add_field(name = "**Lovers [user] [user]**-" , value = "Shows the compatibility between two people!" , inline = False)
    embed.add_field(name = "**Embed**-" , value = "Allows you to make your own embed!" , inline = False)
    embed.add_field(name = "**ask [question]**-" , value = "Play The Administrator's version of 8-Ball!", inline = False)
    embed.add_field(name = "**roll [amount]**-", value = "Rolls a dice with specified range", inline = False)
    embed.add_field(name = "**rr-**" , value = "How lucky are you feeling? Play Russian Roulette to find out!" , inline = False)
    embed.add_field(name = "**avatar [user]**-" , value = "Pulls the pinged user's avatar!", inline = False)
    embed.set_footer(text = f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)
  if criteria == "economy":
    embed = discord.Embed(title = "**Economy Help Menu**" , value = "Help Menu For The Economy!" , color = discord.Color.green())
    embed.add_field(name = "**balance / bal**" , value = "Shows the wallet and bank balance of the author" , inline = False)
    embed.add_field(name = "**withdraw / with [amount]**" , value = "Withdraws the specified amount from the player's bank to the player's wallet!" , inline = False)
    embed.add_field(name = "**deposit / dep [amount**]" , value = "Deposits the specified amount from the player's wallet to the player's bank!" , inline = False)
    embed.add_field(name = "**work**" , value = "Work every 5 minutes to earn some money!" , inline = False)
    embed.add_field(name = "**rob [user]**" , value = "If the user has money in their wallet, you can rob them!" , inline = True)
    embed.add_field(name = "**currency [currency-symbol]**" , value = "Set your server's currency symbol!" , inline = False)
    embed.add_field(name = "**slots [amount]**" , value = "Gamble using the famous slot machine!" , inline = False)
    embed.add_field(name = "**add_money [user] [amount]**" , value = "Adds the amount specified to the bank account of the targeted user. Only works if the author has manage message permissions." , inline = False)
    embed.add_field(name = "**remove_money [user] [amount]**" , value = "Removes the amount specified to the bank account of the targeted user. Only works if the author has manage message permissions." , inline = False)
    await ctx.send(embed = embed)

@client.command()
async def rank(ctx):
  await switch_check(ctx.guild)
  guild = ctx.guild
  user = ctx.author
  with open('level_check.json' , 'r') as f:
    checklevel = json.load(f)
  with open('levels.json' , 'r') as f:
    levels = json.load(f)
  if str(checklevel[f"{guild.id}"]["status"]) == "off":
    errormsg = await ctx.send("Your server's admins have disabled leveling! Please PM them if you believe this is a mistake. This message will self destruct in 5 seconds.")
    await asyncio.sleep(5)
    await ctx.channel.purge(limit = 2)
  elif str(checklevel[f"{guild.id}"]["status"]) == "on":
    embed = discord.Embed(title = f"{ctx.author.name}'s Rank", description = '\n\u200b' , color = discord.Color.purple())
    embed.add_field(name = "**Level**" , value = str(levels[f'{user.id}']['levels']), inline = False)
    embed.add_field(name = "**Exp**" , value = str(levels[f'{user.id}']['experience']), inline = False)
    embed.set_thumbnail(url = user.avatar_url)
    await ctx.send(embed = embed)

@client.command()
@commands.has_permissions(ban_members = True)
async def prefix(ctx, new):
  guild = ctx.guild
  with open("prefix.json" , "r") as f:
    prefix = json.load(f)
  if not f"{guild.id}" in prefix:
    prefix[f"{guild.id}"] = {}
    prefix[f"{guild.id}"]["prefix"] = "-"
  await ctx.send(f"Changed this server's bot prefix to `{new}`.")
  command_prefix2 = prefix[f"{guild.id}"]["prefix"]
  with open("prefix.json", "w") as f:
    prefix = json.dump(prefix, f)

@client.event
async def on_player_join(member):
  with open("levels.json", "r") as f:
    levels = json.load(f)

  await update_data(levels, member)

  
  
  with open("levels.json", "w") as f:
    json.dump(levels, f)

@client.event
async def on_message(message):
  with open("levels.json", "r") as f:
    levels = json.load(f)
  with open("level_check.json" , "r") as f:
    checklevel = json.load(f)
  guild = message.guild
  await switch_check(message.guild)
  if str(checklevel[f"{guild.id}"]["status"]) == "on":
    await update_data(levels, message.author)
    await add_experience(levels, message.author, 5)
    await level_up(levels, message.author, message.channel)
  
    with open("levels.json", "w") as f:
      json.dump(levels, f)
 
    await client.process_commands(message)
  elif str(checklevel[f"{guild.id}"]["status"]) == "off":
    await client.process_commands(message)

    


async def update_data(levels, user):
  if not f'{user.id}' in levels:
    levels[f'{user.id}'] = {}
    levels[f'{user.id}']['experience'] = 0
    levels[f'{user.id}']['levels'] = 1

async def switch_check(guild):
  with open("level_check.json" , "r") as f:
    checklevel = json.load(f)
  if not f'{guild.id}' in checklevel:
    checklevel[f"{guild.id}"] = {}
    checklevel[f"{guild.id}"]["status"] = "off"
    
    
async def add_experience(levels, user, exp):
  if user.id != "897139608196894750":
    levels[f'{user.id}']['experience'] += exp


async def level_up(levels, user, channel):
  experience = levels[f'{user.id}']['experience']
  lvl_start = levels[f'{user.id}']['levels']
  lvl_end = int(experience ** (1/4))

  if lvl_start < lvl_end:
    await channel.send(f"{user.mention}")
    embed = discord.Embed(title = f"**{user.name} has leveled up!**" , description = f"{user.name} is now level {lvl_end}." , color = discord.Color.green())
    embed.set_image(url = "https://c.tenor.com/HJOCluQ5n7kAAAAC/party-time-michael-scott.gif")
    await channel.send(embed=embed)
    levels[f'{user.id}']['levels'] = lvl_end


@client.event
async def on_guild_join(guild):
  with open("currency.json" , "r") as f:
    currency = json.load(f)
  await set_default_currency(guild, currency)

  with open("currency.json", "w") as f:
    json.dump(currency, f)

async def set_default_currency(guild, currency):
  if not f"{guild.id}" in currency:
    currency[f"{guild.id}"] = {}
    currency[f"{guild.id}"]["currency"] = "$"
  
    
@client.command()
async def currency(ctx, currencyswap = "$"):
  with open("currency.json", "r") as f:
    currency = json.load(f)
    guild = ctx.guild
    currency[f"{guild.id}"]["currency"] = currencyswap
  with open("currency.json", "w") as f:
    json.dump(currency, f)
  await ctx.send(f"Success! You have changed your server's currency to {currencyswap}.")

async def check_currency():
  with open("currency.json", "r") as f:
    currency = json.load(f)
    return currency

@client.command()
@commands.has_permissions(manage_messages = True)
async def leveling(ctx, * ,status):
  with open("level_check.json" , "r") as f:
    checklevel = json.load(f)
  guild = ctx.guild
  if status == "on":
    checklevel[f'{guild.id}']["status"] = "on"
    await ctx.send("This server's leveling system is now on!")
  elif status == "off":
    checklevel[f'{guild.id}']["status"] = "off"
    await ctx.send("This server's leveling is now off!")
  else:
    await ctx.send("That isn't a valid expression!")
  with open("level_check.json" , "w") as f:
    checklevel = json.dump(checklevel, f)

  
@client.command(aliases = ['bal'])
async def balance(ctx, * , usered = "self"):
  user = ctx.author
  await open_account(user)

  guild = ctx.guild
  currency = await check_currency()
  users = await get_bank_data()

  currencycheck = currency[f"{guild.id}"]["currency"]
  wallet_bank = users[f"{user.id}"]["wallet"]
  bank_bank = users[f"{user.id}"]["bank"]

  embed = discord.Embed(title = f"**{ctx.author.name}'s Balance**" , color = discord.Color.green())
  embed.add_field(name = "**Wallet**" , value = str(currencycheck) + str(wallet_bank))
  embed.add_field(name = "**Bank**" , value = str(currencycheck) + str(bank_bank))
  await ctx.send(embed=embed)

  

async def open_account(user):
  users = await get_bank_data()

  if not f'{user.id}' in users:
    users[f"{user.id}"] = {}
    users[f"{user.id}"]["wallet"] = 0
    users[f"{user.id}"]["bank"] = 0
  else:
    return False

  with open("money.json" , "w") as f:
    users = json.dump(users, f)

async def get_bank_data():
  with open("money.json" , "r") as f:
    users = json.load(f)
    return users

@client.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
  await open_account(ctx.author)
  users = await get_bank_data()
  currency = await check_currency()
  user = ctx.author
  guild = ctx.guild
  currencycheck = currency[f"{guild.id}"]["currency"]
  embed = discord.Embed(title = "**Daily Bonus**" , description = "Deposited your daily bonus of " + str(currencycheck) + "200 into your wallet!" , color = discord.Color.green())
  embed.set_footer(text = f"{ctx.author.name}")
  await ctx.send(embed = embed)
  users[f"{user.id}"]["wallet"] += 200
  with open("money.json", "w") as f:
    users = json.dump(users , f)

@daily.error
async def daily_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    embed = discord.Embed(title = "**Cooldown**" , description = f"This command is on cooldown, try again in {round(error.retry_after/3600)} hours.", color = discord.Color.red())
    embed.set_footer(text = f"{ctx.author.name}")
    await ctx.send(embed=embed)

@client.command()
@commands.cooldown(1, 1800, commands.BucketType.user)
async def work(ctx):
  await open_account(ctx.author)
  users = await get_bank_data()
  currency = await check_currency()
  user = ctx.author
  guild = ctx.guild
  payment = random.randrange(1000)

  currencycheck = currency[f"{guild.id}"]["currency"]

  workmatrix = [f"You find " + str(currencycheck) + f"{payment} on the sidewalk." , 
f"You work as an extra in an upcoming movie. They pay you " + str(currencycheck) + f"{payment} for your hard work!" , 
f"You help the little old lady cross the street. She gives you " + str(currencycheck) + f"{payment} for being a nice young citizen." ,
f"You sold a youth potion and it flopped. But at least you got " + str(currencycheck) + f"{payment} from it." , 
"You release a game and it went decently well. Ad revenue nets you " + str(currencycheck) + f"{payment}." , 
"A random guy tells you about this pyramid scheme. You try it and it actually works somehow! You gain " + str(currencycheck) + f"{payment}." ,
"You gain " + str(currencycheck) + f"{payment} from streaming on Twitch!" , 
"You work as a babysitter for your neighbors and earn " + str(currencycheck) + f"{payment} for your trouble." ,
"You trick your coworker into pranking you, and you get his bonus of " + str(currencycheck) + f"{payment}.",
"You work as a hired hand, and you earn " + str(currencycheck) + f"{payment} for finding new hands for your client." ,
"You help recover a lost artifact from the days of Columbus. Your cut is " + str(currencycheck) + f"{payment}." , "You work as a grocery store cashier. It got you " + str(currencycheck) + f"{payment}."] 
  embed = discord.Embed(title = "**Work**" , description = random.choice(workmatrix), color = discord.Color.green())
  embed.set_footer(text = f"{ctx.author.name}")
  await ctx.send(embed=embed)    
  
  users[f"{user.id}"]["wallet"] += payment
  
  with open("money.json" , "w") as f:
    users = json.dump(users, f)
      
@work.error
async def work_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    embed = discord.Embed(title = "**Cooldown**" , description = f"This command is on cooldown, try again in {round(error.retry_after/60)} minutes.", color = discord.Color.red())
    embed.set_footer(text = f"{ctx.author.name}")
    await ctx.send(embed=embed)
    
@client.command()
@commands.cooldown(1, 3600, commands.BucketType.user)
async def rob(ctx, victim : discord.Member):
  await open_account(ctx.author)
  await open_account(victim)
  currency = await check_currency()
  guild = ctx.guild
  currencycheck = currency[f"{guild.id}"]["currency"]
  users = await get_bank_data()
  user = ctx.author
  percent = ["yes" , "no" , "no", "no"]
  amount = random.randrange(1000)
  if victim == ctx.author:
    await ctx.send("You can't rob yourself, silly!")
  elif int(users[f"{victim.id}"]["wallet"]) < amount:
    embed = discord.Embed(title = "**Too Poor!**" , description = f"{user.name}, you might want to pick someone less... poor to rob." , color = discord.Color.red())
    embed.set_footer(text = f"{ctx.author.name}")
    await ctx.send(embed=embed)
  elif random.choice(percent) == "yes":
    embed = discord.Embed(title = "**Rob**" , description = f":money_with_wings:You just stole " + str(currencycheck) + f"{amount} from {victim.mention}!:money_with_wings:")
    embed.add_footer(text = f"{ctx.author.name}")
    await ctx.send(embed=embed)
    users[f"{user.id}"]["wallet"] += amount
    users[f"{victim.id}"]["wallet"] -= amount
  elif random.choice(percent) == "no":
    embed = discord.Embed(title = f"**You Were Caught!**" , description = f":rotating_light:{ctx.author.mention} just tried to steal from {victim.mention}! Someone call the cops!:rotating_light:" , color = discord.Color.red())
    embed.set_footer(text = f"{ctx.author.name}")
    await ctx.send(embed=embed)
  with open("money.json" , "w") as f:
    users = json.dump(users, f)

@rob.error
async def rob_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    embed = discord.Embed(title = "**Cooldown**" , description = f"You can only attempt to rob once an hour. Try again in {round(error.retry_after/60)} minutes.", color = discord.Color.red())
    embed.set_footer(text = f"{ctx.author.name}")
    await ctx.send(embed=embed)

@client.command()
async def slots(ctx , amt = 0):
  slotmatrix = [":banana:" , ":apple:", ":gem:" , ":tangerine:" , ":pear:" , ":ring:"]
  slot1 = random.choice(slotmatrix)
  slot2 = random.choice(slotmatrix)
  slot3 = random.choice(slotmatrix)
  slot4 = random.choice(slotmatrix)
  slot5 = random.choice(slotmatrix)
  slot6 = random.choice(slotmatrix)
  slot7 = random.choice(slotmatrix)
  slot8 = random.choice(slotmatrix)
  slot9 = random.choice(slotmatrix)
  await open_account(ctx.author)
  currency = await check_currency()
  guild = ctx.guild
  currencycheck = currency[f"{guild.id}"]["currency"]
  users = await get_bank_data()
  user = ctx.author
  with open("money.json" , "r") as f:
    users = json.load(f)
  
  
  embed = discord.Embed(title = "**Slot Machine**" , description = f"You are waging " + str(currencycheck) + f"**{amt}.**" , color = discord.Color.blue())
  embed.add_field(name = slot1 + " "+slot2 + " "+slot3 , value = "\n\u200b" , inline = False)
  embed.add_field(name = slot4 + " "+slot5+ " "+slot6 , value = "\n\u200b" , inline = False)
  embed.add_field(name = slot7 + " "+slot8 + " "+slot9, value = "\n\u200b" , inline = False)
  if int(amt) > int(users[f"{user.id}"]["wallet"]):
    await ctx.send("You can't bet that much!")
    return
  else:
    await ctx.send(embed=embed)
  if slot1 == slot2 == slot3 or slot4 == slot5 == slot6 or slot7 == slot8 == slot9 or slot1 == slot4 == slot7 or slot2 == slot5 == slot8 or slot3 == slot6 == slot9 or slot1 == slot5 == slot9 or slot3 == slot5 == slot7:
    await ctx.send(f"Way to go! You won " + str(currencycheck) + f"{2*int(amt)}.")
    users[f"{user.id}"]["wallet"] += amt
  elif slot1 == slot2 == slot3 == slot4 == slot5 == slot6 == slot7 == slot8 == slot9:
    await ctx.send("Amazing! You got a blackout. You earned 5x your wage!")
    users[f"{user.id}"]["wallet"] += 5 * int(amt)
  else:
    await ctx.send("Aw. You lost.")
    users[f"{user.id}"]["wallet"] -= amt
    
  with open("money.json" , "w") as f:
    users = json.dump(users, f)

@client.command()
async def give(ctx, recipient : discord.Member , amt = 0):
  await open_account(ctx.author)
  currency = await check_currency()
  guild = ctx.guild
  currencycheck = currency[f"{guild.id}"]["currency"]
  users = await get_bank_data()
  user = ctx.author
  with open("money.json" , "r") as f:
    users = json.load(f)
  if recipient == ctx.author:
    await ctx.send("You can't give money to yourself!")
  elif int(users[f"{user.id}"]["wallet"]) < int(amt):
    await ctx.send("You don't have enough money for that!")
  elif int(users[f"{user.id}"]["wallet"]) >= int(amt):
    users[f"{user.id}"]["wallet"] -= int(amt)
    users[f"{recipient.id}"]["wallet"] += int(amt)
    embed = discord.Embed(title = "**Give**" , description = f"You have given {amt} to {recipient.mention}!" , color = discord.Color.green())
    await ctx.send(embed=embed)
  with open("money.json", "w") as f:
    users = json.dump(users, f)

@client.command(aliases = ['dep'])
async def deposit(ctx, amt):
  await open_account(ctx.author)
  currency = await check_currency()
  guild = ctx.guild
  users = await get_bank_data()
  user = ctx.author
  all = int(users[f"{user.id}"]["wallet"])
  currencycheck = currency[f"{guild.id}"]["currency"]
  if amt.isdigit() and int(users[f"{user.id}"]["wallet"]) >= int(amt):
    users[f"{user.id}"]["bank"] += int(amt)
    users[f"{user.id}"]["wallet"] -= int(amt)
    embed = discord.Embed(title = "**Deposit**" , description = f"Success! You deposited " + str(currencycheck) + f"{amt} into your bank account." , color = discord.Color.green())
    embed.set_footer(text = f"{ctx.author.name}")
    await ctx.send(embed=embed)
  elif amt == "all":
    users[f"{user.id}"]["wallet"] -= all
    users[f"{user.id}"]["bank"] += all
    embed = discord.Embed(title = "**Deposit**" , description = f"Success! You deposited all your money (" + str(currencycheck) + f"{all}) into your bank account!" , color = discord.Color.green())
    embed.set_footer(text = f"{ctx.author.name}")
    await ctx.send(embed=embed)
  elif int(users[f"{user.id}"]["wallet"]) < int(amt):
    embed = discord.Embed(title = "**Deposit Error**" , description = "It seems you don't have enough money in your wallet for that!" , color = discord.Color.red())
    embed.set_footer(text = f"{ctx.author.name}")
    await ctx.send(embed=embed)
  
  with open("money.json" , "w") as f:
    users = json.dump(users, f)


@client.command(aliases = ['with'])
async def withdraw(ctx, amt):
  await open_account(ctx.author)
  currency = await check_currency()
  guild = ctx.guild
  users = await get_bank_data()
  user = ctx.author
  all = int(users[f"{user.id}"]["bank"])
  currencycheck = currency[f"{guild.id}"]["currency"]
  if amt.isdigit() and int(users[f"{user.id}"]["bank"]) >= int(amt):
    users[f"{user.id}"]["bank"] -= int(amt)
    users[f"{user.id}"]["wallet"] += int(amt)
    embed = discord.Embed(title = "**Deposit**" , description = f"Success! You withdrew " + str(currencycheck) + f"{amt} from your bank account." , color = discord.Color.green())
    embed.set_footer(text = f"{ctx.author.name}")
    await ctx.send(embed=embed)
  elif amt == "all":
    users[f"{user.id}"]["bank"] -= int(all)
    users[f"{user.id}"]["wallet"] += int(all)
    embed = discord.Embed(title = "**Withdraw**" , description = f"Success! You withdrew all your money (" + str(currencycheck) + f"{all}) from your bank account!" , color = discord.Color.green())
    embed.set_footer(text = f'{ctx.author.name}')
    await ctx.send(embed=embed)
  elif int(users[f"{user.id}"]["bank"]) < int(amt):
    embed = discord.Embed(title = "**Withdraw Error**" , description = "It seems you don't have enough money in your bank for that!" , color = discord.Color.red())
    embed.set_footer(text = f"{ctx.author.name}")
    await ctx.send(embed=embed)
  
  with open("money.json" , "w") as f:
    users = json.dump(users, f)

@client.command(aliases = ["shop"])
async def store(ctx , action = "shop"):
  currency = await check_currency()
  guild = ctx.guild
  currencycheck = currency[f"{guild.id}"]["currency"]
  with open("store.json" , "r") as f:
    store = json.load(f)
  if not f"{guild.id}" in store:
    store[f"{guild.id}"] = {}
    store[f"{guild.id}"]['items'] = "Nothing here!"
    store[f"{guild.id}"]['descriptions'] = "Not available"
    store[f"{guild.id}"]['price'] = "N/A"
    
""" if action == "shop":  
    embed = discord.Embed(title = "**Store**" , color = discord.Color.blue())
    embed.add_field(name = "**" + store[f"{guild.id}"]['items'] + "** - " + store[f"{guild.id}"]['price'] , value = store[f"{guild.id}"]['descriptions'], inline = False)
    await ctx.send(embed=embed)
  elif action == "create":
    await ctx.send("What would you like the name of your item to be?")
    if ctx.author != ctx.author:
      return
    elif ctx.author == ctx.author:
      itemname = await client.wait_for("message")
      store[f"{guild.id}"]['items'] = itemname.content
      await ctx.send("How much will this cost?")
      itemprice = await client.wait_for("message")
      store[f"{guild.id}"]['price'] = itemprice.content
      await ctx.send("What should the description be?")
      itemdesc = await client.wait_for("message")
      store[f"{guild.id}"]['descriptions'] = itemdesc.content
      await ctx.send("Shop Item Created!")
      with open("store.json" , "w") as f:
        users = json.dump(store, f)"""

@client.command(aliases = ["inv"])
async def inventory(ctx):
  with open("inventory.json", "r") as f:
    inv = json.load(f)
  user = ctx.author
  guild = ctx.guild
  if not f'{user.id}' in inv:
    if not f'{guild.id}' in inv:
      inv[f'{user.id}'] = {}
      inv[f'{user.id}']['inventory'] = "Oops! It looks like your inventory is empty"
      inv[f'{user.id}']['quantity'] = 0
    with open("inventory.json" , "w") as f:
      inv = json.dump(inv, f)
  embed = discord.Embed(title = f"**{ctx.author.name}**'s Inventory" , color = discord.Color.blue())
  embed.add_field(name = "**" + str(inv[f'{user.id}']['inventory']) + "**" , value = "Quantity: " + str(inv[f'{user.id}']['quantity']), inline = False)
  await ctx.send(embed=embed)

@client.command()
async def buy(ctx , val):
  with open("money.json" , "r") as f:
    users = json.load(f)
  user = ctx.author
  users = await get_bank_data()
  guild = ctx.guild
  value = str(val)
  await open_account(ctx.author)
  currency = await check_currency()
  currencycheck = currency[f"{guild.id}"]["currency"]
  if value == store[f'{user.id}']['items']:
    if int(users[f"{user.id}"]["wallet"]) >= int(store[f'{user.id}']['price']):
      await ctx.send(f"Success! You bought 1 " + str(store[f'{user.id}']['items']) + " for " + str(currencycheck) + int(store[f'{user.id}']['price']) + ".")
      users[f"{user.id}"]["wallet"] -= int(store[f'{user.id}']['price'])
      with open("money.json" , "w") as f:
        users = json.dump(users , f)

@client.command()
@commands.has_permissions(manage_messages = True)
async def add_money(ctx , user : discord.Member , amt):
  await open_account(user)
  currency = await check_currency()
  guild = ctx.guild
  users = await get_bank_data()
  amount = int(amt)
  currencycheck = currency[f"{guild.id}"]["currency"]
  users[f"{user.id}"]["wallet"] += amount
  await ctx.send(f"Success! {ctx.author.name} has added " + str(currencycheck) + f"{amount} to {user.name}'s wallet!")
  with open("money.json", "w") as f:
    users = json.dump(users, f)

@client.command()
@commands.has_permissions(manage_messages = True)
async def remove_money(ctx , user : discord.Member , amt):
  await open_account(user)
  currency = await check_currency()
  guild = ctx.guild
  users = await get_bank_data()
  amount = int(amt)
  currencycheck = currency[f"{guild.id}"]["currency"]
  users[f"{user.id}"]["wallet"] -= amount
  await ctx.send(f"Success! {ctx.author.name} has removed " + str(currencycheck) + f"{amount} from {user.name}'s wallet!")
  with open("money.json", "w") as f:
    users = json.dump(users, f)

@client.command()
@commands.has_permissions(manage_messages = True)
async def rules(ctx, * , content = "1) No hacking"):
  embed= discord.Embed(
    title = f"**__{ctx.message.guild.name}__**" , description = "*Server Rules*" , color = discord.Color.purple())
  embed.add_field(name = "\n\u200b" , value = "\n\u200b" + content, inline = True)
  await ctx.channel.purge(limit = 1)
  await ctx.send(embed=embed)
  
  
@client.command()
async def sourcecode(ctx):
  await ctx.send("https://github.com/fighter-Ethan/The-Administrator")

@client.command()
async def rroul(ctx):
  brazild = (random.randint(0 , 6))
  if brazild < 4:
    await ctx.send("*Click*" + "\n\u200b" + "\n\u200b" + random.choice(rrmatrix))
  elif brazild > 5:
    await ctx.send("**BANG!**" + "\n\u200b" + "https://78.media.tumblr.com/80b50d102cdf69e5c172d4cbe336f10d/tumblr_mvc0oeWuPY1qd9rjto1_500.gif")
  elif brazild == 5:
    await ctx.send("**BANG!**" + "\n\u200b" + "https://78.media.tumblr.com/80b50d102cdf69e5c172d4cbe336f10d/tumblr_mvc0oeWuPY1qd9rjto1_500.gif")

@client.command()
async def roll(ctx , * , value = 0):
  await ctx.send(random.randint(0 , value))

  
@client.command(aliases = ["compat" , "lovers"])
async def compatibility(ctx , user : discord.Member , member : discord.Member):
  loverate = random.randint(0 , 100)
  embed = discord.Embed(
  title = ":heart:Compatability Tester:heart:" , description = user.mention + " + " + member.mention, color  = discord.Color.green())
  embed.add_field(name = "Compatability Rate: " , value = str(loverate) + "%", inline = True)
  embed.set_thumbnail(url = "https://www.northeastohioparent.com/wp-content/uploads/2021/01/Cupid.png")
  embed.set_footer(text = "Come up with a good ship name for these two lovebirds!") 
  await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(manage_messages = True)
async def purge(ctx, amount = 1):
	await ctx.channel.purge(limit=amount + 1)


@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, * , reason = "N/A"):
	await member.kick(reason = reason)
	await ctx.send(member.name + " was kicked from the server because: " + reason)

@client.command()
async def avatar(ctx , member : discord.Member):
  embed = discord.Embed(title = member.name + "'s discord Avatar" , color = discord.Color.red())
  embed.set_image(url = member.avatar_url)
  await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="N/A"):
	await member.ban(reason=reason)
	await ctx.send(member.name + " was banned from the server, because: " +
reason)

@client.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx , * , member):
  banned_users = await ctx.guild.bans()
  member_name , member_disc = member.split('#')
  
  for banned_entry in banned_users:
    user = banned_entry.user
    
    if (user.name , user.discriminator) == (member_name , member_disc):
      await ctx.guild.unban(user)
      await ctx.send(member_name + " has been unbanned!")
      return
  
  await ctx.send(member + " was not found!")

@client.command()
@commands.has_permissions(manage_roles = True)
async def accept(ctx , member : discord.Member , role : discord.Role , reason = "No reason inputted!"):
  embed = discord.Embed(title = "Accepted" , description = "Application Feedback" , color = discord.Color.green())
  embed.add_field(name = "**Discord Tag**" , value = member.mention + "\n\u200b" , inline = False)
  embed.add_field(name = "\n\u200b" + "**Department**" , value = role.mention + "\n\u200b" , inline = False)
  embed.add_field(name="\n\u200b" + "**Reason**" , value = reason , inline = False)
  embed.set_thumbnail(url = "https://i.pinimg.com/originals/7b/dd/1b/7bdd1bc7db7fd48025d4e39a0e2f0fd8.jpg")
  embed.set_footer(text = f"Approved by {ctx.author.name}")
  await ctx.channel.purge(limit=1)
  await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(manage_roles = True)
async def deny(ctx , member : discord.Member , role : discord.Role , * , reason = "No reason inputted!"):
  embed = discord.Embed(
    title = "Denied"
   , description = "Application Feedback" , color = discord.Color.red())
  embed.add_field(name = "**Discord Tag**" , value = member.mention + "\n\u200b" , inline = False)
  embed.add_field(name = "\n\u200b" + "**Department**" , value = role.mention + "\n\u200b", inline = False)
  embed.add_field(name="\n\u200b" + "**Reason**" , value = reason , inline = False)
  embed.set_thumbnail(url = "https://cdn.pixabay.com/photo/2012/04/12/20/12/x-30465_640.png")
  embed.set_footer(text = f"Denied by {ctx.author.name}")
  await ctx.channel.purge(limit=1)
  await ctx.send(embed=embed)
    
@client.command()
@commands.has_permissions(administrator = True)
async def announce(ctx, * , content = "No announcement."):
  if content == "No announcement.":
    await ctx.send("No message specified! This will automatically delete in five seconds.")
    await asyncio.sleep(5)
    await ctx.channel.purge(limit = 2)
  else:
    embed = discord.Embed(
    title = "**ANNOUNCEMENT**" , description = f"From {ctx.author.name}" , color = discord.Color.green())
    embed.add_field(name = "\n\u200b" , value = content , inline = True)
    await ctx.channel.purge(limit = 1)
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(send_messages = True)
async def ask(ctx, * , content = "No question" ):
  if content == "No question":
    await ctx.send("There was no question asked!")
  else:
    await ctx.send(random.choice(eightballquestion))
  

@client.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(client.latency * 1000 , 0)) + "ms")

@client.command()
async def poll(ctx , responsetitle = "Poll" , response1 = "N/A" , response2 = "N/A" , response3 = "N/A" , response4 = "N/A"):
  if response1 == "N/A" or response2 == "N/A":
    await ctx.send("You need to input at least two options!")
  else:
    embed = discord.Embed(title = responsetitle , description = f"Requested by {ctx.author.name}" , color = discord.Color.blue())
    embed.add_field(name = '\N{REGIONAL INDICATOR SYMBOL LETTER A}' + response1 , value = "\n\u200b" , inline = False)
    embed.add_field(name = '\N{REGIONAL INDICATOR SYMBOL LETTER B}' + response2 , value = "\n\u200b" , inline = False)
    if response3 != "N/A":
      embed.add_field(name = '\N{REGIONAL INDICATOR SYMBOL LETTER C}' + response3 , value = "\n\u200b" , inline = False)
    if response4 !="N/A":
      embed.add_field(name = '\N{REGIONAL INDICATOR SYMBOL LETTER D}' + response4 , value = "\n\u200b" , inline = False)
    await ctx.channel.purge(limit = 1)
    message = await ctx.send(embed=embed)
    emoji = '\N{REGIONAL INDICATOR SYMBOL LETTER A}'
    emoji2 = '\N{REGIONAL INDICATOR SYMBOL LETTER B}'
    emoji3 = '\N{REGIONAL INDICATOR SYMBOL LETTER C}'
    emoji4 = '\N{REGIONAL INDICATOR SYMBOL LETTER D}'
    await message.add_reaction(emoji)
    await message.add_reaction(emoji2)
    if response3 != "N/A":  
      await message.add_reaction(emoji3)
    if response4 != "N/A":
      await message.add_reaction(emoji4)

@client.command()
async def support(ctx):
  await ctx.send("https://discord.gg/VtfUCjejXq")
  
@client.command()
async def invite(ctx):
  await ctx.send("https://discord.com/api/oauth2/authorize?client_id=799087847310884904&permissions=8&scope=bot%20applications.commands")

@client.command()
async def speak(ctx , * , text = "Hi!"):
  await ctx.channel.purge(limit=1)
  await ctx.send(text)

@client.command()
async def embed(ctx):
  if ctx.guild == ctx.guild:
    await ctx.send("Alright! Let's start with the title. Please enter your title. It will automatically be bolded, so don't worry about that!")
    emb1 = await client.wait_for('message')
    if ctx.author == ctx.author:
      await ctx.channel.purge(limit = 2)
      await ctx.send("Great! Now for the description right under the title!")
      emb2 = await client.wait_for('message')
      if ctx.author == ctx.author:
        await ctx.channel.purge(limit = 2)
        await ctx.send("Got it! Now enter the text you want added!")
        emb3 = await client.wait_for('message')
        if ctx.author == ctx.author:
          await ctx.channel.purge(limit = 2)
          await ctx.send("Finally, add the footer. If you want to skip this, just say 'skip'.")
          emb5 = await client.wait_for('message')
          if ctx.author == ctx.author:
            await ctx.channel.purge(limit = 2)
            embed = discord.Embed(title = "**" + emb1.content + "**" , description = emb2.content , color = discord.Color.red())
            embed.add_field(name = "\n\u200b" , value = emb3.content , inline = True)
            if emb5.content == "skip":
              await ctx.channel.purge(limit = 2)
              await ctx.send(embed=embed)
            else:
              embed.set_footer(text = emb5.content)
              await ctx.channel.purge(limit = 2)
              await ctx.send(embed=embed)

@client.command()
async def kiss(ctx , user : discord.Member):
  if user.mention == "<@799087847310884904>":
    await ctx.send("Sorry, I'm taken :(")
  else:
    embed = discord.Embed(title = f"{ctx.author.name}  kisses " + user.name + "!" , color = discord.Color.red())
    embed.set_image(url = "https://i.pinimg.com/originals/18/ea/9e/18ea9e8b6b921ba7ce0081c48b802670.gif")
    await ctx.send(embed=embed)

@client.command()
async def hit(ctx , user : discord.Member):
  if user.mention == "<@799087847310884904>":
    await ctx.send("You touch me, I scream.")
  else:
    embed = discord.Embed(title = f"{ctx.author.name} hits {user.name}!" , description = "\n\u200b", color = discord.Color.red())
    embed.set_image(url = "https://media1.tenor.com/images/df8af24e5756ecf4a4e8af0c9ea6499b/tenor.gif?itemid=4902917")
    await ctx.send(embed = embed)

@client.command()
async def hug(ctx , user : discord.Member):
  hugmatrix = ["https://www.icegif.com/wp-content/uploads/icegif-6.gif" , ""]
  if user.mention == "<@799087847310884904>":
    await ctx.send("Don't hug me! I don't like hugs :(")
  else:
    embed = discord.Embed(title = f"{ctx.author.name} hugs {user.name}!" , description = "\n\u200b", color = discord.Color.red())
    embed.set_image(url = "https://media.tenor.com/images/ecf4840ba6fac22be773e586493d5283/tenor.gif")
    await ctx.send(embed = embed)

@client.command()
async def boop(ctx , user : discord.Member):
  if user.mention == "<@799087847310884904>":
    await ctx.send("Don't boop me! :(")
  else:
    embed = discord.Embed(title = f"{ctx.author.name} boops {user.name}!" , description = "\n\u200b", color = discord.Color.red())
    embed.set_image(url = "https://media.tenor.com/images/5307e3f5a44d4d510ae58c9e76991f60/tenor.gif")
    await ctx.send(embed = embed)

@client.command()
async def stare(ctx , user : discord.Member):
  starematrix = ["https://media4.giphy.com/media/aXUU30cDBa9tVQz37V/giphy-downsized-large.gif" , "https://media2.giphy.com/media/9V3e2mxWvD89wyw5l5/200w.gif?cid=82a1493btyeb6ypapwfw67u5yjoygqfb8mdxom6lqg15bc5x&rid=200w.gif&ct=g" , "https://media3.giphy.com/media/BY8ORoRpnJDXeBNwxg/200.gif"]
  if user.mention == "<@799087847310884904>":
    await ctx.send("Don't stare at me!")
  else:
    embed = discord.Embed(title = f"{ctx.author.name} stares at {user.name}!" , description = "\n\u200b", color = discord.Color.red())
    embed.set_image(url = random.choice(starematrix))
    await ctx.send(embed = embed)

@client.command()
async def kill(ctx, user : discord.Member):
  await ctx.send("No killing :(")

@client.command()
@commands.has_permissions(ban_members = True)
async def grant(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"Success! {user.name} has been given the role {role.name}.")

@client.command()
@commands.has_permissions(ban_members = True)
async def revoke(ctx , user: discord.Member , role : discord.Role):
  await user.remove_roles(role)
  await ctx.send(f"Success! {user.name} no longer has the {role.name} role!")

@client.command()
@commands.has_permissions(manage_roles=True)
async def rr(ctx, mode = "view"):
  if mode == "view":
    await ctx.send("Please try again.")
  elif mode == "add":
    await ctx.send("Where would you like to add reaction roles?")
    channel_roles_raw = await client.wait_for("message")
    if ctx.author == ctx.author:
      channel_roles = str(channel_roles_raw.content)
      await ctx.send(f"Alright! We will send the reaction role to #{channel_roles}. What would you like the embed title to be?")
      embed_title = await client.wait_for("message")
      if ctx.author == ctx.author:
        await ctx.send("And what color would you like for the embed? Type 'none' to have no color.")
        embed_color = await client.wait_for("message")
        if ctx.author == ctx.author:
          await ctx.send("Perfect. Now, please add the emote you wish to be the reaction and then the role you want associated with it! Please only do one  at a time. Ex: :pleading_face:, then @RandomRole")
          roles_emojis = await client.wait_for("message")
          if ctx.author == ctx.author:
            return

@client.command()
async def log(ctx, status = None, channel_log = None):
  guild = ctx.guild
  with open("logging.json", "r") as f:
    logging = json.load(f)
    
  if not f'{guild.id}' in logging:
    logging[f'{guild.id}'] = {}
    logging[f'{guild.id}']['status'] = "on"
    if channel_log != None:
      logging[f'{guild.id}']['channel_log'] = channel_log
    
  if status == "on":
    logging[f'{guild.id}']['status'] = "on"
    await ctx.send("Status of logging set to on!")
    
  elif status == "off":
    logging[f'{guild.id}']['status'] = "off"
    await ctx.send("Status of logging set to off!")
    
  with open("logging.json" , "w") as f:
    logging = json.dump(logging, f)


@client.event
async def on_message_delete(message):
  with open("logging.json", "r") as f:
    logging = json.load(f)
    
  guild = message.guild
  author : message.author #Defines the message author
  content : message.content #Defines the message content
  channel : message.channel #Defines the message channel
  channel_logs = (logging[f'{guild.id}']['channel_log'])

  if logging[f'{guild.id}']['status'] == "on":
    
    await channel_logs.send("<@{}>'s message was deleted. Message Content: {}".format(message.author.id, message.content))
  if logging[f'{guild.id}']['status'] == "off":
    return
  await client.process_commands(message)

  
  
            
TOKEN = os.environ.get("DISCORD_BOT_SECRET")
client.run(TOKEN)