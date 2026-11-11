# Schema evolution
Alembic manages schema changes under services/api/migrations. POC bootstrap currently uses SQLAlchemy create_all for convenience; before deploying an actual system, remove implicit create_all and run versioned migrations separately with backup/rollback preparation.
From services/api: `alembic upgrade head` and `alembic current`. The pilot branch adds approval tables in revision 0002.
For contract fidelity, validate backward-compatible migrations against a restored synthetic Postgres dataset. The presence of migration scripts does not prove execution on GCP.
