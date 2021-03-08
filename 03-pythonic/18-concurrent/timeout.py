import asyncio
import time

loop = asyncio.get_event_loop()
t0 = time.time()


async def infinite_print():
    while True:
        print(f"{time.time()-t0:.5f}s")
        await asyncio.sleep(0.5)


async def async_main():
    try:
        await asyncio.wait_for(infinite_print(), 3)
    except asyncio.TimeoutError:
        print("fini")


loop.run_until_complete(async_main())
