import asyncio
import random
import time
import requests
import threading
from telethon import TelegramClient, events
from flask import Flask

# --- CONFIG ---
API_ID = 36767235
API_HASH = "6a36bf6c4b15e7eecdb20885a13fc2d7"
BOT_TOKEN = "8791927496:AAEdPeuCO99MgBrh-TLiJ7Q7gAkcFGEGjIU"
OWNER_ID = 7844678082
GIPHY_API_KEY = "YLLksuIyKHZcaMKuAOYR1s27dz2uy8Xr"

# --- LISTES ---
blacklist = {OWNER_ID}
owners = {OWNER_ID}
cooldowns = {}

# --- TELETHON ---
client = TelegramClient('bot_hentai', API_ID, API_HASH)

# --- FLASK ---
app = Flask("")

@app.route("/")
def home():
    return "Bot hentai/slap/kiss en ligne !"

def run_flask():
    app.run(host="0.0.0.0", port=5000)

threading.Thread(target=run_flask).start()

# --- FONCTIONS UTILES ---
def check_blacklist(user_id):
    return user_id in blacklist

def check_owner(user_id):
    return user_id in owners

def is_on_cooldown(user_id):
    return user_id in cooldowns and time.time() - cooldowns[user_id] < 5

def get_cooldown_remaining(user_id):
    if user_id not in cooldowns:
        return 0
    remaining = 5 - (time.time() - cooldowns[user_id])
    return max(0, int(remaining))

def update_cooldown(user_id):
    cooldowns[user_id] = time.time()

def get_giphy_gif(tag):
    url = f"https://api.giphy.com/v1/gifs/random?api_key={GIPHY_API_KEY}&tag={tag}&rating=pg-13"
    resp = requests.get(url).json()
    return resp['data']['images']['original']['url']

# --- LIENS HENTAI ---
hentai_gifs = [
    "https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd459eaf877.gif",
    "https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd459f14394.gif",
    "https://www.cougarillo.com/wp-content/uploads/2023/12/porno-hentai.gif",
    "https://www.cougarillo.com/wp-content/uploads/2023/12/levrette-gif-hentai.gif",
    "https://www.cougarillo.com/wp-content/uploads/2023/12/gif-hentai-gros-seins.gif",
    "https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai145.gif",
    "https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai125.gif",
    "https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai143.gif",
    "https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai129.gif",
    "https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai119.gif",
    "https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai127.gif",
    "https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai122.gif",
    "https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai120.gif",
    "https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai141.gif",
    "https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai139.gif",
    "https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai140.gif",
    "https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai114.gif",
    "https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai123.gif",
    "https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai115.gif",
    "https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai142.gif",
    "https://img2.gelbooru.com//images/40/5f/405f442f0a5b6631821708238aed7d9a.gif",
    # ajoute ici tous les autres liens hentai que tu m’as donnés
]

# --- COMMANDES ---
@client.on(events.NewMessage(pattern=r'\.hentai'))
async def hentai(event):
    user_id = event.sender_id
    if not check_blacklist(user_id):
        return
    remaining = get_cooldown_remaining(user_id)
    if remaining > 0:
        await event.reply(f"😡 Calme-toi un peu, c’est pas le bot à ta mère ! Attends {remaining}s")
        return
    gif = random.choice(hentai_gifs)
    msg = await event.reply(file=gif)
    update_cooldown(user_id)
    await asyncio.sleep(6)
    await msg.delete()

@client.on(events.NewMessage(pattern=r'\.(slap|kiss) @(\w+)'))
async def slap_kiss(event):
    user_id = event.sender_id
    if not check_blacklist(user_id):
        return
    remaining = get_cooldown_remaining(user_id)
    if remaining > 0:
        await event.reply(f"😡 Calme-toi un peu, c’est pas le bot à ta mère ! Attends {remaining}s")
        return
    action = event.pattern_match.group(1)
    username = event.pattern_match.group(2)
    await event.reply(f"{action.upper()} pour @{username} !")
    update_cooldown(user_id)

@client.on(events.NewMessage(pattern=r'\.(slap|kiss)$'))
async def slap_kiss_fail(event):
    await event.reply("❌ Mentionne quelqu’un ! Utilise .slap @user ou .kiss @user")

# --- BLACKLIST ---
@client.on(events.NewMessage(pattern=r'\.bl @(\w+)'))
async def add_bl(event):
    if event.sender_id != OWNER_ID:
        return
    username = event.pattern_match.group(1)
    user = await client.get_entity(username)
    blacklist.add(user.id)
    await event.reply(f"✅ @{username} ajouté à la blacklist")

@client.on(events.NewMessage(pattern=r'\.unbl @(\w+)'))
async def remove_bl(event):
    if event.sender_id != OWNER_ID:
        return
    username = event.pattern_match.group(1)
    user = await client.get_entity(username)
    blacklist.discard(user.id)
    await event.reply(f"❌ @{username} retiré de la blacklist")

@client.on(events.NewMessage(pattern=r'\.blacklist'))
async def show_bl(event):
    msg = "Blacklist :\n"
    for uid in blacklist:
        user = await client.get_entity(uid)
        msg += f"- @{user.username} ({user.first_name})\n"
    await event.reply(msg)

# --- RUN BOT ---
async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("Bot hentai/slap/kiss démarré…")
    await client.run_until_disconnected()

asyncio.run(main())
