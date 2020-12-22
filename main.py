import discord
import asyncio
from discord.ext import commands, tasks
from settings import DISCORD_TOKEN, COMMANDS, PREFIX, UPDATE_TIME

bot = commands.Bot(command_prefix=PREFIX, status=discord.Status.online, help_command=None)


@bot.event
async def on_ready():
    from db_manager import startup
    startup()
    print('Start!')


@bot.command()
async def help(ctx):
    await ctx.send("명령어 목록\n-{}\n-{}\n-{}\n-{}\n-{}".format(
        COMMANDS['poll']['command'],
        COMMANDS['rss_add']['command'],
        COMMANDS['rss_del']['command'],
        COMMANDS['rss_list']['command'],
        COMMANDS['rss_update']['command'],
    ))

def split_messsage(msg):
    return msg.split(' ')


@bot.command(name=COMMANDS['poll']['command'])
async def poll_app(ctx):
    from itertools import cycle
    ICON_SET = cycle([
        (':one:', '\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}'),
        (':two:', '\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}'),
        (':three:', '\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}'),
        (':four:', '\N{DIGIT FOUR}\N{COMBINING ENCLOSING KEYCAP}'),
        (':five:', '\N{DIGIT FIVE}\N{COMBINING ENCLOSING KEYCAP}'),
        (':six:', '\N{DIGIT SIX}\N{COMBINING ENCLOSING KEYCAP}'),
        (':seven:', '\N{DIGIT SEVEN}\N{COMBINING ENCLOSING KEYCAP}'),
        (':eight:', '\N{DIGIT EIGHT}\N{COMBINING ENCLOSING KEYCAP}'),
        (':nine:', '\N{DIGIT NINE}\N{COMBINING ENCLOSING KEYCAP}'),
    ])
    full_msg = ctx.message.content
    lst_msg_token = list(map(lambda x: x.replace("\"", ""), split_messsage(full_msg)))
    if len(lst_msg_token) > 11:
        await ctx.send("도움 메시지 출력")
    else:
        used_emoji = []
        formated_message = f"**{lst_msg_token[1]}**\n"
        for index in range(2, len(lst_msg_token)):
            emoji, unicode = next(ICON_SET)
            formated_message += f"{emoji} : {lst_msg_token[index]}\n"
            used_emoji.append(unicode)

        msg = await ctx.send(formated_message)
        for emoji in used_emoji:
            await msg.add_reaction(emoji)


@bot.command(name=COMMANDS['rss_add']['command'])
async def rss_add_command(ctx):
    from rss_manager import rss_add

    full_msg = ctx.message.content
    lst_msg_token = split_messsage(full_msg)
    if len(lst_msg_token) != 3:
        await ctx.send("도움 메시지 출력")
    else:
        res, msg = rss_add(lst_msg_token[1], lst_msg_token[2])
        if res:
            await ctx.send("성공했습니다.")
            await ctx.add
        else:
            await ctx.send(f"예외가 발생했습니다.\n{msg}")


@bot.command(name=COMMANDS['rss_del']['command'])
async def rss_del_command(ctx):
    from rss_manager import rss_del

    full_msg = ctx.message.content
    lst_msg_token = split_messsage(full_msg)
    if len(lst_msg_token) != 2 and not isinstance(lst_msg_token[1], int):
        await ctx.send("도움 메시지 출력")
    else:
        res, msg = rss_del(lst_msg_token[1])
        if res:
            await ctx.send("성공했습니다.")
        else:
            await ctx.send(f"예외가 발생했습니다.\n{msg}")


@bot.command(name=COMMANDS['rss_list']['command'])
async def rss_list_command(ctx):
    from rss_manager import rss_list

    full_msg = ctx.message.content
    lst_msg_token = split_messsage(full_msg)
    if len(lst_msg_token) > 1:
        await ctx.send("도움 메시지 출력")
    else:
        res, msg = rss_list()
        if msg is None:
            if any(res):
                await ctx.send("\n".join(res))
            else:
                await ctx.send("생성된 rss가 없습니다.")
        else:
            await ctx.send(f"예외가 발생했습니다.\n{msg}")


@bot.command(name=COMMANDS['rss_update']['command'])
async def rss_update_command(ctx):
    from rss_manager import rss_update

    full_msg = ctx.message.content
    lst_msg_token = split_messsage(full_msg)
    if len(lst_msg_token) > 1:
        await ctx.send("도움 메시지 출력")
    else:
        res = rss_update()
        if res is not None:
            for rss in res:
                formated_msg = f"**{rss['rss_title']}**\n```\n*{rss['post_title']}*\n{rss['post_description']}\n{rss['post_published']}```{rss['post_link']}"
                await ctx.send(formated_msg)
        else:
            await ctx.send("추가된 rss가 없습니다.")


async def rss_update_scheduled():
    from rss_manager import rss_update
    await bot.wait_until_ready()
    while not bot.is_closed():
        for channel in bot.get_all_channels():
            if channel.type.name == 'text':
                res = rss_update()
                if res is not None:
                    for rss in res:
                        formated_msg = f"**{rss['rss_title']}**\n```\n*{rss['post_title']}*\n{rss['post_description']}\n{rss['post_published']}```{rss['post_link']}"
                        await channel.send(formated_msg)
        await asyncio.sleep(int(UPDATE_TIME))


bot.loop.create_task(rss_update_scheduled())
bot.run(DISCORD_TOKEN)
