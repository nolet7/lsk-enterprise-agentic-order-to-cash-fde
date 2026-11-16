# Stakeholder discovery: hypotheses and walkthroughs

**Status: proposed scenario, not evidence of completed real-world interviews.**

| Stakeholder | Workflow to walk through | Questions and observed artifact to request | Approval |
|---|---|---|---|
| Commercial / account managers | Quote -> contracted price -> purchase order | Where are price exceptions reconciled? Which account and contract are authoritative? Samples of redacted quote/PO mismatches | Commercial owner |
| Customer service | Order status -> exception -> customer update | Which requests require swivel-chair lookup? Which interactions need agent handoff? Redacted case timelines | CSR lead |
| Supply-chain planning | Promise date -> allocation -> backorder | Who can override available-to-promise? How are split orders and substitutions approved? Exception queue samples | Planning lead |
| Warehouse / logistics | Pick -> ship -> proof of delivery | Where is WMS status delayed? Carrier events, partial shipments, lost events and dispute process | Logistics owner |
| Procurement / supplier quality | Supplier onboard -> credential validity -> release/hold | Required certifications, scope, jurisdiction, expiry, supplier ownership and escalation SLA | Supplier Quality |
| Finance / billing | Ship -> invoice -> credit/dispute | Who owns invoice status and tax? What can be automated without a finance approval? Reconciliation reports | Finance |
| IT / security | Events, identity, API gateways, audit | Versions, rate limits, OIDC scopes, data classification, event replay, recovery, PII retention | IT/Security |

## AS-IS workflow (illustrative, validate in discovery)
1. Commercial checks contract terms in ERP or spreadsheets and asks the pricing owner about differences.
2. CSR manually checks ERP order state and WMS shipment state, then sends customer updates.
3. Supply Chain reviews allocation/backorder exceptions in separate queues; operator reconciles stale updates.
4. Procurement/Quality verifies supplier documents manually before approving supplier-related exceptions.
5. Finance checks shipment and invoice mismatches, manually routes credits/disputes.
6. IT handles point-to-point mapping failures, replay and access requests.

## TO-BE workflow (target)
Customer portal/CSR console -> authenticated tenant-aware API gateway -> orchestration and policy -> read from authoritative ERP/CRM/WMS/billing/supplier services -> classify exceptions -> deterministic validation -> human approval where required -> idempotent write -> outbox/event/status reconciliation -> audit and notifications. The agent is never an unreviewed system of record.

## Baseline measurement sheet (fill with real data only after authorization)
| Metric | Definition | Baseline | Target | Source/owner |
|---|---|---|---|---|
| Manual touches/order | Human handoffs per order lifecycle | TBD | Agree in discovery | Commercial/CSR |
| Exception resolution p95 | Ticket creation to verified resolution | TBD | Agree in pilot | Supply Chain |
| On-time fulfillment | Delivered on/before committed date / eligible orders | TBD | Agree in pilot | WMS/Logistics |
| Supplier credential checks | Manual checks / supplier release request | TBD | Agree in pilot | Supplier Quality |
| Integration reconciliation errors | Mismatched canonical entities by day | TBD | Agree in pilot | IT/Data |
| Unauthorized write rate | Unauthorized writes that succeed | Not yet measured | 0 (hard gate) | Security |

## Workshop output / signoff form
Date: TBD; participants and role: TBD; workflow version: TBD; source-of-truth owner: TBD; open assumptions: TBD; signed decisions: TBD; next owner/date: TBD. Never record fictional approvals as actual.
