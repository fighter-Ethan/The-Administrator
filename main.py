#Imports
import discord
import discord.utils
from discord.ext import commands
from discord.utils import get
import asyncio
from webserver import keep_alive
import os
import json
import requests
import random

#Commands Handler- DO NOT TOUCH
client = commands.Bot(command_prefix="-")
member = discord.Member

#Removes the default help command. The Administrator has his own!
client.remove_command('help')

#Matrixes
eightballquestion = [":8ball:Ask again later" , ":8ball:For sure!" , ":8ball:Absolutely not." , ":8ball:Not sure yet." , ":8ball:Perhaps." , ":8ball:Absolutely!"]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + ' -' + json_data[0]['a']
  return(quote)

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name= "over " +  str(len(client.guilds)) + " servers | -help"))
  print('Bot is ready!')

@client.command()
async def help(ctx):
  embed = discord.Embed(
    title="Help Page",
    description="The list of commands for The Administrator", color = discord.Color.red())
  embed.add_field(name = "**Purge [amount]**-" , value = 'Purges selected amount of messages' + "\n\u200b" , inline = True)
  embed.add_field(name = "**Kick [user] [reason]**-" , value = 'Kicks the selected member and displays the reason' + "\n\u200b" , inline = True)
  embed.add_field(name = "**Ban [user] [reason]**-" , value = "Bans the selected member and displays the reason" + "\n\u200b" , inline = True)
  embed.add_field(name = "**Accept [user] [role] [reason]**-" , value = "Sends a message in the current channel notifying others of your decision to promote" + "\n\u200b" , inline = True)
  embed.add_field(name = "**Deny [user] [role] [reason]**-" , value = "Sends a message in the current channel notifying others of your decision to demote" + "\n\u200b" , inline = True)
  embed.add_field(name = "**Announce [message]**-" , value = "Sends an announcement in the current channel" + "\n\u200b" , inline = True)
  embed.add_field(name = "**Lovers [user] [user]**-" , value = "Shows the compatibility between two people!" + "\n\u200b" , inline = True)
  embed.add_field(name = "**Kiss [user]**-" , value = "Kisses the specified player" + "\n\u200b" , inline = True)
  embed.add_field(name = "**Embed**-" , value = "Allows you to make your own embed!" + "\n\u200b" , inline = True)
  embed.add_field(name = "**Invite**-" , value = "Sends an invite link so you can add The Administrator to your server!" + "\n\u200b" , inline = True)
  embed.add_field(name = "**Support**-" , value = "Sends an invite to The Administrator Support server!" + "\n\u200b")
  embed.add_field(name = "**Grant [user] [role]**-" , value = "Grants selected user the role you specify." + "\n\u200b" , inline = True)
  embed.set_thumbnail(url= ctx.author.avatar_url)
  embed.set_footer(text=f"Requested by {ctx.author.name}. Join the support server by typing -support!")
  await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(manage_messages = True)
async def rules(ctx, * , content = "1) No hacking"):
  embed= discord.Embed(
    title = f"**__{ctx.message.guild.name}__**" , description = "*Server Rules*" , color = discord.Color.purple())
  embed.add_field(name = "\n\u200b" , value = "\n\u200b" + content, inline = True)
  await ctx.channel.purge(limit = 1)
  await ctx.send(embed=embed)
  
@client.command()
async def kiss(ctx , * , kisses = "themself. Weird"):
  embed = discord.Embed(title = f"{ctx.author.name}  kisses " + kisses + "!" , color = discord.Color.red())
  embed.set_image(url = "https://www-irishtimes-com.cdn.ampproject.org/i/s/www.irishtimes.com/polopoly_fs/1.3380702.1517841297!/image/image.jpg_gen/derivatives/landscape_620/image.jpg")
  await ctx.send(embed=embed)

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
@commands.has_permissions(manage_messages = True)
async def accept(ctx , member : discord.Member , role : discord.Role , * , reason = "No reason inputted!"):
  embed = discord.Embed(
    title = "Accepted"
   , description = "Staff Team Application" , color = discord.Color.green())
  embed.add_field(name = "**Discord Tag**" , value = member.mention + "\n\u200b" , inline = True)
  embed.add_field(name = "\n\u200b" + "**Department**" , value = role.mention + "\n\u200b" , inline = True)
  embed.add_field(name="\n\u200b" + "**Reason**" , value = reason , inline = True)
  embed.set_thumbnail(url = "https://i.pinimg.com/originals/7b/dd/1b/7bdd1bc7db7fd48025d4e39a0e2f0fd8.jpg")
  embed.set_footer(text = f"Approved by {ctx.author.name}")
  await ctx.channel.purge(limit=1)
  await ctx.send(embed=embed)

@client.command()
async def check(msg):
  return msg.author == ctx.author and msg.channel == ctx.channel


@client.command()
@commands.has_permissions(manage_messages = True)
async def dmaccept(ctx , member : discord.Member):
  await ctx.send("Please put the Department!")
  dma = await client.wait_for('message' , check = check)
  await ctx.send("Now the reason...")
  dma2 = await client.wait_for('message' , check = check)
  embed = discord.Embed(
    title = "Accepted"
   , description = f"Staff Team of {ctx.guild.name}" , color = discord.Color.green())
  embed.add_field(name = "**Discord Tag**" , value = member.mention + "\n\u200b" , inline = True)
  embed.add_field(name = "\n\u200b" + "**Department**" , value = dma.content + "\n\u200b" , inline = True)
  embed.add_field(name="\n\u200b" + "**Reason**" , value = dma2.content , inline = True)
  embed.set_thumbnail(url = "https://i.pinimg.com/originals/7b/dd/1b/7bdd1bc7db7fd48025d4e39a0e2f0fd8.jpg")
  embed.set_footer(text = f"Approved by {ctx.author.name}")
  await ctx.channel.purge(limit=5)
  await member.send(embed=embed)

@client.command()
@commands.has_permissions(manage_messages = True)
async def dmdeny(ctx , member : discord.Member):
  await ctx.send("Please put the Department!")
  dma3 = await client.wait_for('message' , check = check)
  await ctx.send("Now the reason...")
  dma4 = await client.wait_for('message' , check = check)
  embed = discord.Embed(
    title = "Denied"
   , description = f"Staff Team of {ctx.guild.name}" , color = discord.Color.red())
  embed.add_field(name = "**Discord Tag**" , value = member.mention + "\n\u200b" , inline = True)
  embed.add_field(name = "\n\u200b" + "**Department**" , value = dma3.content + "\n\u200b" , inline = True)
  embed.add_field(name="\n\u200b" + "**Reason**" , value = dma4.content , inline = True)
  embed.set_thumbnail(url = "hhttps://cdn.pixabay.com/photo/2012/04/12/20/12/x-30465_640.png")
  embed.set_footer(text = f"Denied by {ctx.author.name}")
  await ctx.channel.purge(limit=5)
  await member.send(embed=embed)

@client.command()
@commands.has_permissions(ban_members = True)
async def deny(ctx , member : discord.Member , role : discord.Role , * , reason = "No reason inputted!"):
  embed = discord.Embed(
    title = "Denied"
   , description = "Staff Team Application" , color = discord.Color.red())
  embed.add_field(name = "**Discord Tag**" , value = member.mention + "\n\u200b" , inline = True)
  embed.add_field(name = "\n\u200b" + "**Department**" , value = role.mention + "\n\u200b")
  embed.add_field(name="\n\u200b" + "**Reason**" , value = reason , inline = True)
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
  await ctx.send("How many options would you like to be in your poll? You can have a minimum of 2 and a maximum of 4.")
  wait4 = await client.wait_for("message")
  if wait4.content == "4":
    embed = discord.Embed(title = responsetitle , description = f"Requested by {ctx.author.name}" , color = discord.Color.blue())
    embed.add_field(name = '\N{REGIONAL INDICATOR SYMBOL LETTER A}' + response1 , value = "\n\u200b" , inline = True)
    embed.add_field(name = '\N{REGIONAL INDICATOR SYMBOL LETTER B}' + response2 , value = "\n\u200b" , inline = True)
    embed.add_field(name = '\N{REGIONAL INDICATOR SYMBOL LETTER C}' + response3 , value = "\n\u200b" , inline = True)
    embed.add_field(name = '\N{REGIONAL INDICATOR SYMBOL LETTER D}' + response4 , value = "\n\u200b" , inline = True)
    await ctx.channel.purge(limit = 3)
    message = await ctx.send(embed=embed)
    emoji = '\N{REGIONAL INDICATOR SYMBOL LETTER A}'
    emoji2 = '\N{REGIONAL INDICATOR SYMBOL LETTER B}'
    emoji3 = '\N{REGIONAL INDICATOR SYMBOL LETTER C}'
    emoji4 = '\N{REGIONAL INDICATOR SYMBOL LETTER D}'
    await message.add_reaction(emoji)
    await message.add_reaction(emoji2)
    await message.add_reaction(emoji3)
    await message.add_reaction(emoji4)
  elif wait4.content == "3":
    embed = discord.Embed(title = responsetitle , description = f"Requested by {ctx.author.name}" , color = discord.Color.blue())
    embed.add_field(name = '\N{REGIONAL INDICATOR SYMBOL LETTER A}' + response1 , value = "\n\u200b" , inline = True)
    embed.add_field(name = '\N{REGIONAL INDICATOR SYMBOL LETTER B}' + response2 , value = "\n\u200b" , inline = True)
    embed.add_field(name = '\N{REGIONAL INDICATOR SYMBOL LETTER C}' + response3 , value = "\n\u200b" , inline = True)
    await ctx.channel.purge(limit = 3)
    message = await ctx.send(embed=embed)
    emoji5 = '\N{REGIONAL INDICATOR SYMBOL LETTER A}'
    emoji6 = '\N{REGIONAL INDICATOR SYMBOL LETTER B}'
    emoji7 = '\N{REGIONAL INDICATOR SYMBOL LETTER C}'
    await message.add_reaction(emoji5)
    await message.add_reaction(emoji6)
    await message.add_reaction(emoji7)
  elif wait4.content == "2":
    embed = discord.Embed(title = responsetitle , description = f"Requested by {ctx.author.name}" , color = discord.Color.blue())
    embed.add_field(name = '\N{REGIONAL INDICATOR SYMBOL LETTER A}' + response1 , value = "\n\u200b" , inline = True)
    embed.add_field(name = '\N{REGIONAL INDICATOR SYMBOL LETTER B}' + response2 , value = "\n\u200b" , inline = True)
    await ctx.channel.purge(limit = 3)
    message = await ctx.send(embed=embed)
    emoji8 = '\N{REGIONAL INDICATOR SYMBOL LETTER A}'
    emoji9 = '\N{REGIONAL INDICATOR SYMBOL LETTER B}'
    await message.add_reaction(emoji8)
    await message.add_reaction(emoji9)

@client.command()
async def support(ctx):
  await ctx.send("https://discord.gg/dDVtfmQYBv")
  
@client.command()
async def invite(ctx):
  await ctx.send("https://tinyurl.com/4cj3y5uw")

@client.command()
@commands.has_permissions(manage_messages = True)
async def speak(ctx , * , text = "Hi!"):
  await ctx.channel.purge(limit=1)
  await ctx.send(text)

@client.command()
async def encourage(ctx):
  quote = get_quote()
  await ctx.send( '"' + quote + '"')

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
async def smack(ctx , user : discord.Member):
  await ctx.send(f"{ctx.author.name} smacks {user.name}")


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

@client.event
async def on_message(message):
  if client.user.id != message.author.id:
    if 'Hello there' in message.content:
      await message.channel.send('https://thumbs.gfycat.com/FreshGleamingFulmar-max-1mb.gif')
    elif "Pina Colada" in message.content:
      await message.channel.send("If you like pina coladas" + "\n\u200b" + "And gettin' caught in the rain" + "\n\u200b" + "If you're not into yoga" + "\n\u200b" + "If you have half a brain" + "\n\u200b" + "If you like makin' love at midnight" + "\n\u200b" + "In the dunes on the cape" + "\n\u200b" + "Then I'm the love that you've looked for" + "\n\u200b" + "Write to me and escape")
    elif "Pina colada" in message.content:
     await message.channel.send("If you like pina coladas" + "\n\u200b" + "And gettin' caught in the rain" + "\n\u200b" + "If you're not into yoga" + "\n\u200b" + "If you have half a brain" + "\n\u200b" + "If you like makin' love at midnight" + "\n\u200b" + "In the dunes on the cape" + "\n\u200b" + "Then I'm the love that you've looked for" + "\n\u200b" + "Write to me and escape")
    elif "pina colada" in message.content:
      await message.channel.send("If you like pina coladas" + "\n\u200b" + "And gettin' caught in the rain" + "\n\u200b" + "If you're not into yoga" + "\n\u200b" + "If you have half a brain" + "\n\u200b" + "If you like makin' love at midnight" + "\n\u200b" + "In the dunes on the cape" + "\n\u200b" + "Then I'm the love that you've looked for" + "\n\u200b" + "Write to me and escape")
    elif "Lets get down to business" in message.content:
      await message.channel.send("To defeat" + "\n\u200b" "The Huns!")
    elif "Dead chat" in message.content:
      await message.channel.send("https://tse1.mm.bing.net/th?id=OIP.Ak8t-KbA6dNJja1aIUyaEAHaE8&pid=Api&P=0&w=251&h=168")
    elif "hard" in message.content:
      await message.channel.send("That's what she said")
    await client.process_commands(message)

keep_alive()
TOKEN = os.environ.get("DISCORD_BOT_SECRET")
client.run(TOKEN)
