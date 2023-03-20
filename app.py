from telethon import TelegramClient, events
import os
from dotenv import load_dotenv
load_dotenv()

api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')
bot_token = os.getenv('bot_token')

client = TelegramClient('iammrnewtonbot', api_id, api_hash)
client.start(bot_token=bot_token)

@client.on(events.NewMessage)
async def handler(event):
  user = event.sender_id
  await event.respond(event.raw_text)


client.run_until_disconnected()