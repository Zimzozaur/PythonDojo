import asyncio


async def produce_work(
        batch: list[dict],
        work_queue: asyncio.Queue,
        producer_completed: asyncio.Event
):
    for data in batch:
        await work_queue.put(data)

    producer_completed.set()
