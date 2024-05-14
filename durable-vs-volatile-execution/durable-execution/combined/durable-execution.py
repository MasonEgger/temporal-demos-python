import asyncio
import logging
import sys

from temporalio import exceptions, workflow
from temporalio.client import Client, WorkflowExecutionStatus
from temporalio.worker import Worker

logging.basicConfig(level=logging.INFO)

workflow.logger.workflow_info_on_message = False

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)


@workflow.defn
class MyWorkflow:
    @workflow.run
    async def run(self) -> str:
        for i in range(0, 10):
            workflow.logger.info(i)
            await asyncio.sleep(1)

        return "Finished"


async def main():

    try:
        client = await Client.connect("localhost:7233")

        async with Worker(client, task_queue="hello", workflows=[MyWorkflow]):
            result = await client.execute_workflow(
                MyWorkflow.run,
                id="hello",
                task_queue="hello",
            )
    except asyncio.exceptions.CancelledError:
        sys.exit(0)
    except exceptions.WorkflowAlreadyStartedError as err:
        async with Worker(client, task_queue="hello", workflows=[MyWorkflow]):
            workflow_handle = client.get_workflow_handle("hello")
            description = await workflow_handle.describe()
            while description.status != WorkflowExecutionStatus.COMPLETED:
                description = await workflow_handle.describe()
                await asyncio.sleep(1)
    # Catch Ctrl-C so we can limit excessive output in terminal
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
