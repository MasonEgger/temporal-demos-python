import asyncio
import logging
import sys

from businesslogic import CountingWorkflow
from shared import TASK_QUEUE_NAME
from temporalio.client import Client


async def main():
    if len(sys.argv) != 2:
        print("Must specify limit argument!")
        sys.exit(1)

    limit = int(sys.argv[1])

    # Customize the logger output to match the print statement
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )

    client = await Client.connect("localhost:7233")

    output = await client.start_workflow(
        CountingWorkflow.run,
        limit,
        id="counting-workflow-id",
        task_queue=TASK_QUEUE_NAME,
    )

    return output


if __name__ == "__main__":
    asyncio.run(main())
