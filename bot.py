import re
import io
import time
from multiprocessing.pool import ThreadPool
from urllib import request
import os

import discord
from discord.ext import commands

from build import get_build
from rune_image import makeImage
from runes import get_runes

game = discord.Game("!op help")
bot = commands.Bot(command_prefix = '!op', strip_after_prefix = True, activity = game)

@bot.event
async def on_ready():
    '''
    Prints to owner in console when bot is ready.
    '''
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def opgg(ctx, *args):
    
    print("opgg command triggered")
    arg_len = len(args)
    regions = ['oce', 'na', 'las', 'jp', 'br', 'tr', 'ru', 'eune', 'kr', 'lan', 'euw']
    default_region = regions[10]
    async with ctx.typing():
        if arg_len == 0:
            # no args given, check discord name in defualt region
            name = str(ctx.message.author).split('#')[0]
            if default_region == 'kr':
                await ctx.send(f"https://www.op.gg/summoner/userName={name}")
            else:
                await ctx.send(f"https://{default_region}.op.gg/summoner/userName={name}")

        elif arg_len >= 2 and args[0].lower() in regions:
            # big name, region specified
            name = re.sub(r'\s', r'+', ' '.join(args[1:]))
            if args[0].lower() == 'kr':
                await ctx.send(f"https://www.op.gg/summoner/userName={name}")
            else:
                await ctx.send(f"https://{args[0].lower()}.op.gg/summoner/userName={name}")

        elif arg_len >= 1:
            # big name, no region specified
            name = re.sub(r'\s', r'+', ' '.join(args[0:]))
            await ctx.send(f"https://oce.op.gg/summoner/userName={name}")

        else:
            await ctx.send(f"Usage: /opgg [region](optional) [name]")

@bot.command()
async def build(ctx, *args):
    print('Build cmd detected')
    if len(args) != 2:
        await ctx.send('Usage: !op build [lane] [champion]')
    elif args[0] not in ['top', 'mid', 'jungle', 'adc', 'support']:
        await ctx.send('Sorry, can\'t recognise this lane :confused:')
    else:
        async with ctx.typing():
            URL = "https://euw.op.gg/champion/" + args[1] + "/statistics/" + args[0]
            hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
            req = request.Request(URL,headers=hdr)
            res = request.urlopen(req)
            if res.code != 500 and res.url != "https://euw.op.gg/champion/statistics":

                game = discord.Game("Looking for an op build...")
                await bot.change_presence(status = discord.Status.do_not_disturb, activity = game)

                runes = get_runes(args[0], args[1])
                if (len(runes) == 0):
                    await ctx.send('No builds found :(')
                    game = discord.Game("!op help")
                    await bot.change_presence(status = discord.Status.online, activity = game)
                    return

                p1 = ThreadPool(processes = 4).apply_async(makeImage, (runes, ))
                p2 = ThreadPool(processes = 4).apply_async(get_build, (args[0], args[1]))
                rune_img = p1.get()
                data = p2.get()

                await ctx.send(f'Lane: {args[0].capitalize()}')
                await ctx.send(f'Champ: {args[1].capitalize()}')

                builds = data['builds']
                send = ''
                for num in range(len(builds)):
                    send += f'Build {num + 1}: '
                    for item in builds[num]:
                        send += item[0] + ', '
                    send += '\n'
                    send = re.sub(r'(,)[\s]$', '', send)
                await ctx.send(send)

                # send runes
                with io.BytesIO() as image_binary:
                    rune_img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(
                        file=discord.File(
                            fp=image_binary,
                            filename=f'{args[1]} runes.png'
                        )
                    )

                game = discord.Game("!op help")
                await bot.change_presence(status = discord.Status.online, activity = game)
            else:
                await ctx.send('Don\'t worry, Riot will release ' + args[1].capitalize() + ' soon :grin:')

bot.remove_command('help')
@bot.command()
async def help(ctx):
    print("help command triggered")
    async with ctx.typing():
        embed = discord.Embed(
            title="Commands",
            url="https://github.com/mattlau1/Kevin-Nguyen-Bot", color=0x0f7ef5
        )
        embed.add_field(
            name="!op build [lane] [champion]",
            value=(
                """
                Sends most common builds for champion in specified lane.\n
                Lanes: [ top | mid | jg | adc | sup ]
                """
            )
        )
        embed.add_field(
            name="!op opgg [region](optional) [name]",
            value=(
                """
                Sends OP.GG page.\n
                Defaults to Discord username if no name or region specified.\n
                Available Regions: [ oce | na | las | jp | br | tr | ru | eune | kr | lan | euw ]
                """
            )
        )
        await ctx.send(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))
