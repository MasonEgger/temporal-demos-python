import asyncio
import logging
import sys

from businesslogic import CountingWorkflow
from shared import TASK_QUEUE_NAME
from temporalio.client import Client
from temporalio.worker import Worker


async def main():
    logging.basicConfig(level=logging.INFO)
    client = await Client.connect("localhost:7233", namespace="default")

    try:
        worker = Worker(
            client,
            task_queue=TASK_QUEUE_NAME,
            workflows=[CountingWorkflow],
        )
        logging.info(f"Starting the worker....{client.identity}")
        await worker.run()
    except asyncio.exceptions.CancelledError:
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
