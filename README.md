# orders-api

Small FastAPI + sqlite orders service for tracking customer orders.

## Quick start

```bash
mise trust
mise install
./check-tools.sh
uv sync
pytest -q
```

Endpoints on the clean baseline:

- `GET /orders` — list the twenty seed orders
- `GET /orders/{id}` — fetch one order (parameterised SQL)

Terraform lives in `infra/` (AWS provider 6.x, Terraform 1.17). `main.tf` starts empty on purpose.
