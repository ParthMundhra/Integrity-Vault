## Docker Setup (`docker/`)

The `docker/` directory contains configuration for running the core services of the Blockchain‑Backed Tamper‑Proof Digital Forensics & Chain‑of‑Custody System locally using Docker.

### Files

- `Dockerfile`
  - Builds a Python 3.11 image for the **backend** FastAPI service.
  - Installs dependencies from `backend/requirements.txt`.
  - Runs the API with Uvicorn on port `8000`.

- `docker-compose.yml`
  - Defines a multi‑container stack including:
    - **backend** – FastAPI service exposing the REST API.
    - **postgres** – PostgreSQL database for evidence metadata and application state.
    - **ganache** – Local Ethereum node for smart contract development and testing.
  - Connects all services on a shared `forensics-net` bridge network.

### Running the Stack Locally

From the repository root:

```bash
cd docker
docker compose up --build
```

This will:

- Build and start the backend service on `http://localhost:8000`.
- Start PostgreSQL on `localhost:5432` with the `forensics_db` database.
- Start Ganache on `http://localhost:8545` for contract deployment and testing.

Use `docker compose down` to stop and remove the containers when finished. For persistent development environments, you can extend the compose file with volumes and environment overrides as needed.
