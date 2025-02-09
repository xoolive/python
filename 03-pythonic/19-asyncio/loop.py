import asyncio
import time

loop = asyncio.get_event_loop()
t0 = time.time()


def print_now():
    print(f"{time.time() - t0:.5f}s")


loop.call_soon(print_now)  # ①
loop.call_soon(print_now)
loop.run_until_complete(asyncio.sleep(3))  # ②

print(f"fini: {time.time() - t0:.5f}s")

# Exemple du trampoline

t0 = time.time()


def print_trampoline():
    print(f"{time.time()-t0:.5f}s")
    loop.call_later(0.5, print_trampoline)  # ③


loop.call_later(3, loop.stop)  # ④
loop.call_soon(print_trampoline)
loop.run_forever()