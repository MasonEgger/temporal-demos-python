import asyncio

from temporalio import workflow


@workflow.defn
class CountingWorkflow:
    # Make the logging output look more like that of print()
    workflow.logger.workflow_info_on_message = False

    @workflow.run
    async def run(self, limit: int) -> None:
        workflow.logger.info("*** Counting to %d" % limit)

        number = 1
        while number <= limit:
            workflow.logger.info(number)
            number = number + 1
            await asyncio.sleep(1)

        workflow.logger.info("*** Counted to %d" % limit)
