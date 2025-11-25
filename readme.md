
# Bandcamp Sales ETL (Python + PostgreSQL + Docker)

This repository contains a simple ETL(Extract Transform Load) pipeline that ingests a large Bandcamp sales CSV into PostgreSQL, performs transformations and aggregations with pandas, and publishes results.

Stack overview:
- Language: Python
- Libraries: `pandas`, `sqlalchemy` (requires a PostgreSQL DBAPI such as `psycopg2-binary`)
- Database: PostgreSQL (Dockerized)

## Overview

Main scripts:
- `ingest.py` — loads `1000000-bandcamp-sales.csv` into a PostgreSQL table named `raw_data`.
- `transform.py` — reads from `raw_data`, performs cleaning and transformations, prints analytics, and writes the result to a `production` table.
- `publish.py` — (TODOS NOT IMPLEMENTED YET)

`run_pipeline.py` orchestrates the flow:
1) starts the PostgreSQL container via Docker Compose,
2) runs `ingest.py`, `transform.py`, and `publish.py` in order.


## Requirements

- Docker Desktop with Docker Compose v2
- Python 3.x with `pip`. (Tested with Python 3.14)
- Python packages:
  - `pandas`
  - `sqlalchemy`
  - `psycopg2-binary` (PostgreSQL driver used by SQLAlchemy)
- Data file [1000000-bandcamp-sales.csv](https://www.kaggle.com/datasets/mathurinache/1000000-bandcamp-sales) present in the project root..


## Setup

1) Clone the repository and open a terminal at the project root.

2) (Recommended) Create and activate a virtual environment:

   - Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```

   - macOS/Linux (bash/zsh):
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3) Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
   OR
   ```bash
   pip install pandas sqlalchemy psycopg2-binary
   ```

4) Ensure Docker Desktop is running.

5) Place the CSV file [1000000-bandcamp-sales.csv](https://www.kaggle.com/datasets/mathurinache/1000000-bandcamp-sales) in the project root.


## Running

You can run the full pipeline with the provided runner script:

```bash
python run_pipeline.py
```

Alternatively, you can manage services manually:

- Start the DB only:
  ```bash
  docker compose up -d
  ```

## Configuration and Environment Variables

The PostgreSQL container is built from the local `Dockerfile`, which sets:

```dockerfile
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=secure_password
ENV POSTGRES_DB=1000000_bandcamp_sales
```

`ingest.py` and `transform.py` connect using this URL:

```
postgresql://admin:secure_password@localhost:5432/1000000_bandcamp_sales
```

## Scripts

- `run_pipeline.py` — orchestrates Docker and ETL scripts.
- `ingest.py` — reads `1000000-bandcamp-sales.csv` and appends to `raw_data`.
- `transform.py` — cleans/transforms from `raw_data`, prints analytics, and appends to `production`.
- `publish.py` — (TODOS NOT IMPLEMENTED YET)

## Project Structure

```
Dockerfile
docker-compose.yaml
ingest.py
publish.py
run_pipeline.py
transform.py
Readme.md
```
