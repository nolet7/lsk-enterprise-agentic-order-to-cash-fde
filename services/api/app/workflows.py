"""Temporal synthetic delivery exception escalation example."""
from datetime import timedelta
from temporalio import workflow, activity
@activity.defn
async def open_delivery_exception_ticket(tenant_id:str,order_id:str)->str:
    # A real CRM adapter call must be provided before production use.
    return f"SYNTHETIC-TICKET:{tenant_id}:{order_id}"
@workflow.defn
class DeliveryExceptionWorkflow:
    @workflow.run
    async def run(self,tenant_id:str,order_id:str)->str:
        return await workflow.execute_activity(open_delivery_exception_ticket,args=[tenant_id,order_id],start_to_close_timeout=timedelta(seconds=10),retry_policy=None)
