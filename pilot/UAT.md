# Customer UAT protocol (all synthetic)
Participants: grocery buyer A, foodservice buyer B, CSR A, business owner and security reviewer.
Cases: signed OIDC buyer login, contract price lookup, visible only own invoices and orders, draft review and explicit confirmation, repeat idempotency, changed inventory response, lookup of other-tenant ID -> 404, prompt injection refusal, delivery exception -> human ticket, CSR approval queue, revoked identity, outage transparency.
Capture timestamps, actual pass/fail, screenshots, environment, request IDs and signed signoff. Target >=90% scripted tasks, **100% isolation and unauthorized-write tests**. No signoff recorded.
