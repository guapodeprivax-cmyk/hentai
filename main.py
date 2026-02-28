import asyncio
from telethon import TelegramClient, events
from flask import Flask
import threading
import time

# --- CONFIGURATION ---
API_ID = 36767235
API_HASH = "ton_api_hash"
BOT_TOKEN = "8791927496:AAEdPeuCO99MgBrh-TLiJ7Q7gAkcFGEGjIU"
OWNER_ID = 7844678082  # Seul vrai owner

# --- LISTES ---
blacklist = {OWNER_ID}  # Seuls ces utilisateurs peuvent utiliser les commandes
owners = {OWNER_ID}

# --- COOLDOWNS ---
cooldowns = {}  # {user_id: timestamp}

# --- INITIALISATION DU BOT ---
client = TelegramClient('bot_hentai', API_ID, API_HASH)

# --- FLASK SERVER (Render) ---
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
    now = time.time()
    return user_id in cooldowns and now - cooldowns[user_id] < 5

def update_cooldown(user_id):
    cooldowns[user_id] = time.time()

# --- COMMANDES ---
@client.on(events.NewMessage(pattern=r'\.hentai'))
async def hentai(event):
    if not check_blacklist(event.sender_id):
        return
    msg = await event.reply("GIF hentai ici")  # mettre URL ou fichier réel
    await asyncio.sleep(6)
    await msg.delete()

@client.on(events.NewMessage(pattern=r'\.kiss @(\w+)'))
async def kiss(event):
    if not check_blacklist(event.sender_id):
        return
    if is_on_cooldown(event.sender_id):
        await event.reply("⏳ Patiente 5 secondes avant de réutiliser cette commande !")
        return
    username = event.pattern_match.group(1)
    user = await client.get_entity(username)
    await event.reply(f"{event.sender.first_name} embrasse @{username} 💋")
    update_cooldown(event.sender_id)

@client.on(events.NewMessage(pattern=r'\.slap @(\w+)'))
async def slap(event):
    if not check_blacklist(event.sender_id):
        return
    if is_on_cooldown(event.sender_id):
        await event.reply("⏳ Patiente 5 secondes avant de réutiliser cette commande !")
        return
    username = event.pattern_match.group(1)
    user = await client.get_entity(username)
    await event.reply(f"{event.sender.first_name} frappe @{username} 👋")
    update_cooldown(event.sender_id)

# Gestion erreurs si mention manquante
@client.on(events.NewMessage(pattern=r'\.kiss$'))
async def kiss_error(event):
    if check_blacklist(event.sender_id):
        await event.reply("❌ Mentionne quelqu’un avec @ pour utiliser .kiss !")

@client.on(events.NewMessage(pattern=r'\.slap$'))
async def slap_error(event):
    if check_blacklist(event.sender_id):
        await event.reply("❌ Mentionne quelqu’un avec @ pour utiliser .slap !")

# --- GESTION BLACKLIST / OWNER ---
@client.on(events.NewMessage(pattern=r'\.bl @(\w+)'))
async def bl(event):
    if not check_owner(event.sender_id):
        return
    username = event.pattern_match.group(1)
    user = await client.get_entity(username)
    blacklist.add(user.id)
    await event.reply(f"✅ @{username} ajouté à la blacklist")

@client.on(events.NewMessage(pattern=r'\.unbl @(\w+)'))
async def unbl(event):
    if not check_owner(event.sender_id):
        return
    username = event.pattern_match.group(1)
    user = await client.get_entity(username)
    blacklist.discard(user.id)
    await event.reply(f"❌ @{username} retiré de la blacklist")

@client.on(events.NewMessage(pattern=r'\.blacklist'))
async def show_blacklist(event):
    if not check_owner(event.sender_id):
        return
    msg = "Blacklist :\n"
    for uid in blacklist:
        user = await client.get_entity(uid)
        msg += f"- @{user.username} ({user.first_name})\n"
    await event.reply(msg)

# --- DÉMARRAGE DU BOT ---
async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("Bot hentai/slap/kiss démarré…")
    await client.run_until_disconnected()

asyncio.run(main())
