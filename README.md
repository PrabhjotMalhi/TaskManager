# TaskFlow Manager

A lightweight task management tool designed for small teams and individuals to organize, track, and prioritize tasks.

## Features

- Create, edit, delete, and assign tasks
- Text-based reporting of task status
- Google Calendar integration for deadline synchronization
- REST API for third-party integrations
- Cloud-based PostgreSQL storage with daily backups
- Task filtering by status and deadline

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
# Database configuration
export DB_NAME=taskflow
export DB_USER=your_username
export DB_PASSWORD=your_password
export DB_HOST=your_host
export DB_PORT=5432

# Google Calendar API
# Place your credentials.json file in the root directory
```

3. Initialize the database:
```bash
# The application will automatically create necessary tables on first run
```

## Usage

1. Start the API server:
```bash
uvicorn app.api:app --reload
```

2. CLI Interface:
```bash
python app/main.py
```

3. API Endpoints:
- POST /tasks/ - Create a new task
- GET /tasks/ - List tasks (with optional status and deadline filters)
- PUT /tasks/{task_id}/complete - Mark task as complete
- DELETE /tasks/{task_id} - Delete a task

## Architecture

- CLI Application: Handles user input and task creation
- API Module: Provides REST endpoints for external integrations
- Task Manager: Implements business logic and data validation
- Database Handler: Manages PostgreSQL interactions
- Calendar Sync: Handles Google Calendar integration

## Requirements

- Python 3.8+
- PostgreSQL 12+
- Google Calendar API credentials
- AWS RDS for PostgreSQL (production deployment)
