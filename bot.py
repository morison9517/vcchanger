import discord
from discord.ext import commands, tasks
from datetime import datetime
import os
from dotenv import load_dotenv

# .envファイルから環境変数をロード
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('DISCORD_GUILD_ID'))
CHANNEL_ID = int(os.getenv('DISCORD_VC_CHANNEL_ID'))

intents = discord.Intents.default()
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

# タスクを定義して、VCの名前を変更する関数を呼び出す
@tasks.loop(minutes=5)  # 5分ごとに実行
async def update_vc_name():
    now = datetime.now()
    current_hour = now.hour

    guild = bot.get_guild(GUILD_ID)
    vc = guild.get_channel(CHANNEL_ID)

    if 5 <= current_hour < 10:
        new_name = "朝活"
    elif 10 <= current_hour < 18:
        new_name = "昼活"
    elif 18 <= current_hour < 22:
        new_name = "夜活"
    else:
        return  # 対象時間外は変更しない

    await vc.edit(name=new_name)
    print(f"VC name changed to {new_name}")

# ボットが起動した時にタスクを開始
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    update_vc_name.start()  # タスク開始

# Botを実行
bot.run(TOKEN)
