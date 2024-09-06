import asyncio
from typing import Callable


async def handle_task_result(
    result_queue: asyncio.Queue,
    callback: Callable[[dict], None]
):
    while True:
        result = await result_queue.get()
        callback(result)
        result_queue.task_done()

