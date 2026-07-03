# Doblet

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Tkinter](https://img.shields.io/badge/UI-Tkinter-success)
![MariaDB](https://img.shields.io/badge/Database-MariaDB-blue)
![Docker](https://img.shields.io/badge/Container-Docker-2496ED)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![Status](https://img.shields.io/badge/Status-Legacy-orange)

Doblet is a desktop application built in Python for managing the daily operations of the Falla Sants Patrons. It is designed to help handle members, families, categories, fees, lotteries, raffles, histories, and reports in a more efficient and automated way.

## Overview

Doblet provides a practical administrative tool for a traditional association with a large number of members. It helps reduce manual work and improves the consistency of recurring tasks such as:

- Registering and updating members
- Organizing members into families and categories
- Creating new annual exercise periods
- Assigning raffles and lotteries
- Recording payments and movements
- Maintaining historical records and balances
- Generating reports and printable lists

## Project status

This project is now considered legacy. It was originally created as a standalone desktop solution, but the work has since continued in newer projects with the same purpose, namely Doblet Back and Doblet Front. For that reason, this repository will no longer receive further development and no more commits will be made here.

## Technologies used

- Python 3
- Tkinter for the graphical interface
- Pillow for image handling
- reportlab for PDF report generation
- mysql-connector-python for MariaDB access
- MariaDB as the database engine
- Docker Compose for local database setup

## Project structure

- app/: main application code, windows, logic, and business classes
- db/: SQL scripts for database creation, procedures, triggers, and backups
- docker-compose.yml: configuration to run MariaDB and Grafana locally

## Main features

### Member management
- Add, update, and remove members
- Associate members with a family and category
- Store personal and contact information

### Exercise management
- Create a new annual exercise period
- Automatically calculate fees based on category and family discounts
- Track assigned payments and balances

### Lotteries and raffles
- Assign lotteries and raffles manually or automatically
- Record payments and related benefits

### Reports and lists
- Generate administrative reports and lists
- Export documents in PDF format

## Requirements

- Python 3.9 or higher
- MariaDB or Docker for the database layer
- pip
- A virtual environment is recommended

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd Doblet
```

2. Create and activate a virtual environment:

On Windows:

```bash
py -m venv .venv
.venv\Scripts\activate
```

On Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r app/requirements.txt
```

4. Create a .env file at the project root with your database settings:

```env
MYSQL_HOST=localhost
MYSQL_DATABASE=sp
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
MYSQL_ROOT_PASSWORD=your_root_password
```

5. Start the database with Docker Compose:

```bash
docker compose up -d
```

6. Run the application:

On Windows:

```bash
py app\application.pyw
```

On Linux/macOS:

```bash
python3 app/application.pyw
```

## Database

The database is managed through SQL scripts located in the db/ folder. The main schema is defined in db/database_creation.sql, and additional procedures and triggers are stored in the procedures/ and triggers/ subfolders.

### Default database name

- Database name: sp
- The application is prepared to create or initialize the schema if it does not exist.
- Backup scripts are also included in db/dump/.

## Environment variables

The application reads configuration values from a .env file at the project root. This helps avoid hardcoding database credentials in source code.

## Notes

- The project is intended for local and administrative use.
- The current connection setup depends on MariaDB and local environment configuration.
- For shared or production environments, credentials and security settings should be reviewed carefully.

## Author

Developed by Ivan Mas Presentación.
