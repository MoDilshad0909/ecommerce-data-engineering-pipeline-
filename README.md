# End-to-End E-Commerce Data Engineering Pipeline

## Project Overview
This project is a complete data engineering pipeline built to extract, transform, and load (ETL) e-commerce data into a Data Warehouse. It uses Python, PostgreSQL, Apache Airflow, and Power BI to derive meaningful business insights.

## Architecture

Data Sources -> Python ETL -> Staging -> Data Warehouse -> Power BI

## Repository Structure
- `data/`: Local storage for raw and processed datasets (Ignored by Git).
- `sql/`: DDL, DML, and Ad-Hoc SQL queries for the PostgreSQL database.
- `etl/`: Python scripts organized into Extract, Transform, and Load modules.
- `dags/`: Apache Airflow DAGs for pipeline orchestration.
- `dashboard/`: Power BI dashboard files (`.pbix`).
- `docs/`: Project documentation and architecture diagrams.
- `config/`: Configuration settings and environment variables.
- `logs/`: Application and pipeline logs.
- `tests/`: Unit and integration tests.

## Prerequisites
- Python 3.9+
- PostgreSQL
- Apache Airflow (Docker recommended)
- Power BI Desktop

## Setup Instructions
1. Clone the repository
2. Set up a Python virtual environment: `python -m venv venv`
3. Install dependencies: `pip install -r requirements.txt` (to be created)
4. Configure your `.env` file in the `config/` directory.

## License
MIT License
