# Commercial operations discovery pack

**Scenario:** LSK, a fictional B2B wholesale distributor. These are **engineering discovery templates and illustrative hypotheses**, not records of actual stakeholder interviews, production usage, or measured savings. No real customer/supplier information is included.

## Why this pack exists
The mandate is to identify manual order management, fulfillment, and supplier-compliance steps jointly with Commercial, Supply Chain, and IT; define system-of-record ownership; and make the automation plan independently testable. This pack distinguishes *discovery proposed* from *stakeholder validated* and *implemented*.

## Navigation
1. [Stakeholder discovery and current/target journeys](STAKEHOLDER_DISCOVERY.md)
2. [Prioritized functional and nonfunctional requirements](REQUIREMENTS.md)
3. [ERP/CRM/WMS/billing and supplier integration plan](INTEGRATION_PLAN.md)
4. [Supplier compliance control design](SUPPLIER_COMPLIANCE.md)
5. [Requirement-to-test traceability and delivery gates](TRACEABILITY.md)

## Interview protocol (not yet conducted)
Meet Commercial/Account Management, Customer Service, Supply Chain/Planning, Procurement/Supplier Quality, Warehouse/Logistics, Finance/Billing, Security/IAM, Enterprise Integration, and Data Governance. For each workflow collect: trigger; current owner; input/output; manual handoffs; volume and peak pattern; cycle time (p50/p95); error/rework and exception rates; source system; approval authority; privacy classification; retention; and failure/rollback path. Capture dated notes and stakeholder approval in an access-controlled evidence repository, not fabricated transcripts.

## Decision rights
- Commercial signs off pricing/contract and customer-facing journey.
- Supply Chain and Supplier Quality sign off allocation, shipping exceptions and supplier release rules.
- IT/Security signs off API ownership, identity, tenant isolation, integrations, SLOs and DR.
- Finance signs off invoices, tax, credits and reconciliation.
- Product owner accepts the cross-functional scope and residual risks.

## Scope boundaries
POC uses synthetic fixtures and mocks; pilot requires connected system owners and signed UAT; production requires deployment evidence, contracts, control effectiveness and operating signoff. AI can assist with retrieval, triage and drafting; deterministic services own prices, stock, orders, compliance status and payment state. See existing ../ARCHITECTURE.md and ../ACCEPTANCE.md.

## Evidence rule
Mark items **Proposed / Validated / Implemented / Tested / Approved** independently. A design document is *not* proof of implementation; target thresholds are not measurements. Do not imply a real deployment from an infrastructure template.
