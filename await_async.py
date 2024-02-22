import asyncio
import secrets
import time

from asyncio.events import AbstractEventLoop
from collections.abc import Awaitable
from dataclasses import dataclass


@dataclass
class AsyncWaitLoopTiming:
    total_run_time: float
    sum_of_delays: int


async def sleep_for_random_time() -> int:
    delay_time: int = secrets.randbelow(10)
    await asyncio.sleep(delay_time)
    return delay_time


async def loop_await() -> AsyncWaitLoopTiming:
    all_waits: list[Awaitable[int]] = []
    total_wait: int = 0
    start: float = time.perf_counter_ns()
    for _ in range(10):
        all_waits.append(sleep_for_random_time())
    for wait_time in await asyncio.gather(*all_waits):
        total_wait += wait_time
    end: float = time.perf_counter_ns()
    return AsyncWaitLoopTiming(total_run_time=end - start,
                               sum_of_delays=total_wait)


async def wait_in_loop() -> AsyncWaitLoopTiming:
    total_wait: int = 0
    start: float = time.perf_counter_ns()
    for _ in range(10):
        total_wait += await sleep_for_random_time()
    end: float = time.perf_counter_ns()
    return AsyncWaitLoopTiming(total_run_time=end - start,
                               sum_of_delays=total_wait)


if __name__ == "__main__":
    event_loop: AbstractEventLoop = asyncio.new_event_loop()
    loop_wait: AsyncWaitLoopTiming = event_loop.run_until_complete(loop_await())
    bad_async_time: AsyncWaitLoopTiming = event_loop.run_until_complete(wait_in_loop())
    # 1 second has 1,000,000,000 nanoseconds
    ns_to_s_divider: float = 1_000_000_000
    print(f"Total Run Time: {loop_wait.total_run_time / ns_to_s_divider} seconds, "
          f"Sum of random delays: {loop_wait.sum_of_delays} seconds")
    print(f"Total Run Time: {bad_async_time.total_run_time / ns_to_s_divider} seconds, "
          f"Sum of random delays: {bad_async_time.sum_of_delays} seconds")
