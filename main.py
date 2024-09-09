import sys
import time
import asyncio
import subprocess

from pyrogram import Client, filters


api_id = "17103351"
api_hash = "90553f0af0565accb28ebf8833cc6d39"


session = sys.argv[1]

async def main():
    async with Client(session, api_id, api_hash) as app:
        while True:
            with open(f'{session}matn.txt') as matn:
                matn = matn.read()
            with open(f'{session}vaqt.txt') as timefile:
                timeout = int(timefile.read())
            with open('groups.txt') as groups:
                groups = groups.read().split('\n')
                for group in groups:
                    try:
                        await app.send_message(int(group), text=matn)
                    except:
                        pass
            time.sleep(timeout)
                    
asyncio.run(main())
