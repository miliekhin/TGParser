import sys
import os
import requests
from dotenv import load_dotenv

from telethon import TelegramClient, events
from telethon.sessions import StringSession
from tester import *
from settings import TG_CHAT, RESULT_BAD_MSG
from processor import get_final_object


load_dotenv()  # take environment variables from .env.
api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
sess_id = os.environ.get("SESS_ID")
SOURCE_CHANNEL = os.environ.get("SOURCE_CHANNEL")

client = TelegramClient(StringSession(sess_id), int(api_id), api_hash)


@client.on(events.NewMessage(chats='granicaRF2DPR'))
async def handler_new_message(event):
    # Обработчик новых сообщений

    try:
        # event.message содержит информацию о новом сообщении
        # print(event)
        print(f'\n--------------------------------\n{event.message.date}: {event.message.message}')
        result_obj = get_final_object(event.message.message)

        if result_obj['recognition_result'] == RESULT_BAD_MSG:
            print('Message is bad.')
            return
        else:
            print('Sending request to API endpoint...')
            r = requests.post('http://kppshka:8000/api/v1/telega_parser/', data=result_obj)
            print('Response:', r)

            if result_obj['cars_num'] > 200:
                print('Sending warning to MSGS group')
                ent = await client.get_entity('MSGS')
                print('Entity:', ent)
                await client.send_message(entity=ent, message=event.message.message)

    except Exception as e:
        print(e)


# async def main():
#     channel = await client.get_entity(TG_CHAT)
#     print(channel.stringify())


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'run_tests':
        test_get_final_object(None)
    else:
        print(r"""
      ___         ___                   ___         ___         ___         ___         ___         ___     
     /\  \       /\  \                 /\  \       /\  \       /\  \       /\  \       /\  \       /\  \    
     \:\  \     /::\  \               /::\  \     /::\  \     /::\  \     /::\  \     /::\  \     /::\  \   
      \:\  \   /:/\:\  \             /:/\:\  \   /:/\:\  \   /:/\:\  \   /:/\ \  \   /:/\:\  \   /:/\:\  \  
      /::\  \ /:/  \:\  \           /::\~\:\  \ /::\~\:\  \ /::\~\:\  \ _\:\~\ \  \ /::\~\:\  \ /::\~\:\  \ 
     /:/\:\__/:/__/_\:\__\         /:/\:\ \:\__/:/\:\ \:\__/:/\:\ \:\__/\ \:\ \ \__/:/\:\ \:\__/:/\:\ \:\__\
    /:/  \/__\:\  /\ \/__/         \/__\:\/:/  \/__\:\/:/  \/_|::\/:/  \:\ \:\ \/__\:\~\:\ \/__\/_|::\/:/  /
   /:/  /     \:\ \:\__\                \::/  /     \::/  /   |:|::/  / \:\ \:\__\  \:\ \:\__\    |:|::/  / 
   \/__/       \:\/:/  /                 \/__/      /:/  /    |:|\/__/   \:\/:/  /   \:\ \/__/    |:|\/__/  
                \::/  /                            /:/  /     |:|  |      \::/  /     \:\__\      |:|  |    
                 \/__/                             \/__/       \|__|       \/__/       \/__/       \|__|                                                                                                           
                """)
        print('Waiting for new telegram messages...')
        client.start()
        client.run_until_disconnected()

