import asyncio
from random import random
from time import perf_counter


async def do_work(work_queue: asyncio.Queue, result_queue: asyncio.Queue):
    while True:
        task_data = await work_queue.get()

        task_id = task_data['task_id']
        number = task_data['number']

        start = perf_counter()
        await asyncio.sleep(random() * 2)
        result = number * number
        end = perf_counter()

        await result_queue.put(
            {
                "task_id": task_id,
                "result": result,
                "time_secs": end - start
            }
        )

        work_queue.task_done()

        
