from dotenv import load_dotenv
from telethon import TelegramClient, events
import os
import requests
from tqdm import tqdm
from uuid import uuid4
import cryptg
import time
from FastTelethonhelper import fast_download, fast_upload, upload_file

load_dotenv()

api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')
bot_token = os.getenv('bot_token')

client = TelegramClient('test', api_id, api_hash)
client.start(bot_token=bot_token)


def convert_bytes(num_bytes):
    for unit in ['bytes', 'KB', 'MB', 'GB']:
        if num_bytes < 1024.0:
            return f"{num_bytes:.2f} {unit}"
        num_bytes /= 1024.0


async def progress_callback(current, total, chat_id, msg_id):
    progress = f'{round(current / total * 100, 1)}%'
    new_message = f'Uploading... {progress}\n{convert_bytes(current)} of {convert_bytes(total)}'
    await client.edit_message(chat_id, msg_id, new_message)


@client.on(events.NewMessage)
async def handler(event):
    user = event.sender_id
    text = event.raw_text

    if 'http' in text:
        url = text
        filename = str(uuid4())+'.mp4'
        msg = await event.respond('Processing...')
        download(filename=filename, url=url)
        start_time = time.time()
        f = await fast_upload(client, filename, lambda current, total: progress_callback(
            current, total, event.chat_id, msg.id),
        )
        print("--- %s seconds ---" % (time.time() - start_time))
        secondtme = time.time()
        file = await client.upload_file(
            file=filename,
            progress_callback=lambda current, total: progress_callback(
                current, total, event.chat_id, msg.id),
            part_size_kb=512,


        )
        print("--- %s seconds ---" % (time.time() - secondtme))
        await client.send_file(
            user, file,
            progress_callback=lambda current, total: progress_callback(
                current, total, event.chat_id, msg.id),
            force_document=True,

        )
        print('done uploading')


def download(url, filename):

    response = requests.get(url, stream=True)

    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte

    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
    with open(filename, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)

    progress_bar.close()

    if total_size != 0 and progress_bar.n != total_size:
        print("ERROR, something went wrong while downloading!")
    else:
        print("Downloaded successfully!")


client.run_until_disconnected()
