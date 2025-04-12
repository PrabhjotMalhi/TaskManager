import psycopg2
from datetime import datetime
from models import Task
import os
from dotenv import load_dotenv
import subprocess
from typing import List
from pathlib import Path

# Load environment variables from .env file
load_dotenv(dotenv_path=Path('.') / '.env')

class DatabaseHandler:
    def __init__(self):
        self.conn = None
        self.cursor = None
        # Get connection details from environment variables for security
        self.db_config = {
            'dbname': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT')
        }

    def connect(self):
        """Connect to PostgreSQL database"""
        print(f"Attempting to connect to database: {self.db_config['dbname']} at {self.db_config['host']}:{self.db_config['port']} with user {self.db_config['user']}")
        self.conn = psycopg2.connect(**self.db_config)
        self.cursor = self.conn.cursor()
        self._create_tables()
        self._setup_backup()

    def _create_tables(self):
        """Create necessary database tables"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                deadline TIMESTAMP NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                completed BOOLEAN DEFAULT FALSE
            )
        ''')
        self.conn.commit()

    def _setup_backup(self):
        """Setup daily database backups"""
        # Skip backup setup on Windows
        if os.name == 'nt':  # Windows
            return
            
        backup_script = f"""
        #!/bin/bash
        BACKUP_DIR="/var/backups/taskflow"
        mkdir -p $BACKUP_DIR
        pg_dump -h {self.db_config['host']} -U {self.db_config['user']} {self.db_config['dbname']} > $BACKUP_DIR/backup_$(date +%Y%m%d).sql
        find $BACKUP_DIR -type f -mtime +7 -delete
        """
        # Save backup script
        with open('/etc/cron.daily/taskflow-backup', 'w') as f:
            f.write(backup_script)
        # Make it executable
        os.chmod('/etc/cron.daily/taskflow-backup', 0o755)

    def add_task(self, task: Task) -> int:
        """Add a new task to the database"""
        self.cursor.execute('''
            INSERT INTO tasks (title, description, deadline, created_at, completed)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        ''', (task.title, task.description, task.deadline, task.created_at, task.completed))
        task_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return task_id

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks"""
        self.cursor.execute('SELECT * FROM tasks')
        rows = self.cursor.fetchall()
        return [
            Task(
                id=row[0],
                title=row[1],
                description=row[2],
                deadline=row[3],
                created_at=row[4],
                completed=row[5]
            )
            for row in rows
        ]

    def update_task(self, task: Task):
        """Update an existing task"""
        self.cursor.execute('''
            UPDATE tasks
            SET title=%s, description=%s, deadline=%s, completed=%s
            WHERE id=%s
        ''', (task.title, task.description, task.deadline, task.completed, task.id))
        self.conn.commit()

    def delete_task(self, task_id: int):
        """Delete a task"""
        self.cursor.execute('DELETE FROM tasks WHERE id=%s', (task_id,))
        self.conn.commit()

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
