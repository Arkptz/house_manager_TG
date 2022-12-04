from TG.bot import start_bot
from Api.api import start_server
import multiprocessing
from time import sleep
import asyncio

def start_tg_bot():
    start_bot()
def start_api():
    start_server()

if __name__ == "__main__":
    t2 = multiprocessing.Process(target=start_api)
    t2.start()
    t1 = multiprocessing.Process(target=start_tg_bot)
    t1.start()
    try:
        while True:pass
    except KeyboardInterrupt:
        t1.kill()
        t2.kill()
    except:
        pass