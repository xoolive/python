import math

from datetime import datetime
from concurrent.futures import (
    Future,
    ProcessPoolExecutor,
    ThreadPoolExecutor,
    as_completed,
)
import sys

if sys.version_info < (3, 13):
    import _xxsubinterpreters as subinterpreters
else:
    import _interpreters as subinterpreters


def est_premier(n: int) -> bool:
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def compte_premiers(start, end) -> int:
    count = 0
    for i in range(start, end):
        if est_premier(i):
            count += 1
    return count


def premiers_threads(N: int):
    num_threads = 4
    step = N // num_threads
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures: dict[Future, int] = dict()
        results: dict[int, bool] = dict()
        for i in range(num_threads):
            s = i * step
            end = (i + 1) * step if i != num_threads - 1 else N
            futures[executor.submit(compte_premiers, s, end)] = s
        for future in as_completed(futures):
            results[futures[future]] = future.result()


def premiers_multiprocess(N: int):
    num_threads = 4
    step = N // num_threads
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures: dict[Future, int] = dict()
        results: dict[int, bool] = dict()
        for i in range(num_threads):
            s = i * step
            end = (i + 1) * step if i != num_threads - 1 else N
            futures[executor.submit(compte_premiers, s, end)] = s
        for future in as_completed(futures):
            results[futures[future]] = future.result()


def premiers_subinterpreters(N: int):
    CODE = """
import math

def est_premier(n: int) -> bool:
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def compte_premiers(start, end) -> int:
    count = 0
    for i in range(start, end):
        if est_premier(i):
            count += 1
    return count

compte_premiers({start}, {end})
    """
    num_threads = 4
    step = N // num_threads

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        results = []
        for i in range(num_threads):
            s = i * step
            end = (i + 1) * step if i != num_threads - 1 else N
            test = CODE.format(start=s, end=end)

            def f():
                sid = subinterpreters.create()
                subinterpreters.run_string(sid, test)

            futures.append(executor.submit(f))
        for future in as_completed(futures):
            results.append(future.result())


def main():
    N = 10**6

    start = datetime.now()
    compte_premiers(0, N)
    duration = datetime.now() - start
    reference = duration
    print(f"séquentiel         {duration}")

    start = datetime.now()
    premiers_threads(N)
    duration = datetime.now() - start
    print(f"multi-thread       {duration}  {reference/duration:.3f}x")

    start = datetime.now()
    premiers_subinterpreters(N)
    duration = datetime.now() - start
    print(f"interpréteurs      {duration}  {reference/duration:.3f}x")

    start = datetime.now()
    premiers_multiprocess(N)

    duration = datetime.now() - start
    print(f"multi-processus    {duration}  {reference/duration:.3f}x")


if __name__ == "__main__":
    main()
