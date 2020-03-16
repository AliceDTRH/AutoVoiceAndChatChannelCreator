from discord.ext import commands
import os

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='?', description=description)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")


def test_bot_exists():
    assert(bot)

@bot.event
async def on_voice_state_update(member, before, after):
    if bot.get_cog('Util_Commands'):
        util = bot.get_cog('Util_Commands')
        await util.on_voice_state_update(member, before, after)


bot.run(os.environ['DISCORD_ACCESS_TOKEN'])
