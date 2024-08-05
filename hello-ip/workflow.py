from datetime import timedelta

from temporalio import workflow

# Import activity, passing it through the sandbox without reloading the module
with workflow.unsafe.imports_passed_through():
    from activities import WhereAmIActivities


@workflow.defn
class GetAddressFromIP:
    @workflow.run
    async def run(self, name: str) -> str:
        ip_address = await workflow.execute_activity_method(
            WhereAmIActivities.get_ip,
            start_to_close_timeout=timedelta(seconds=5),
        )

        location = await workflow.execute_activity_method(
            WhereAmIActivities.get_location_info,
            ip_address,
            start_to_close_timeout=timedelta(seconds=5),
        )

        return f"Hello {name}. Your IP is {ip_address} and your location is {location}"
