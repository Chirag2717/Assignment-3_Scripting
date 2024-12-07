# Author Name: Chirag Khurana
# Student ID: 100949693
# Assignment 3



import schedule   
import os
import shutil
from datetime import datetime, timedelta
import time

def create_backup(source_dir, backup_dir, retention_days):
    """Create a timestamped backup and manage retention policy."""
    try:
        # Ensure the source directory exists
        if not os.path.exists(source_dir):
            raise FileNotFoundError(f"Source directory '{source_dir}' does not exist.")

        # Ensure the backup directory exists
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Create a timestamped backup folder
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        backup_subdir = os.path.join(backup_dir, f"backup_{timestamp}")
        shutil.copytree(source_dir, backup_subdir)
        print(f"Backup created at {backup_subdir}.")

        # Retention policy: Remove backups older than retention_days
        cutoff_time = datetime.now() - timedelta(days=retention_days)
        for folder in os.listdir(backup_dir):
            folder_path = os.path.join(backup_dir, folder)
            if os.path.isdir(folder_path):
                folder_time = datetime.strptime(folder.split('_')[-1], '%Y%m%d%H%M%S')
                if folder_time < cutoff_time:
                    shutil.rmtree(folder_path)
                    print(f"Old backup removed: {folder_path}")

    except Exception as e:
        print(f"Error during backup: {e}")

def schedule_backup(source_dir, backup_dir, retention_days, backup_time):
    """Schedule the backup process to run daily."""
    schedule.every().day.at(backup_time).do(create_backup, source_dir, backup_dir, retention_days)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    SOURCE_DIR = '/path/to/database/files'  # Replace with the path to your database files
    BACKUP_DIR = '/path/to/backup/location'  # Replace with your backup destination
    RETENTION_DAYS = 7  # Number of days to retain backups
    BACKUP_TIME = "02:00"  # Schedule time for daily backups (24-hour format)

    print(f"Scheduling backups from {SOURCE_DIR} to {BACKUP_DIR} at {BACKUP_TIME} daily.")
    schedule_backup(SOURCE_DIR, BACKUP_DIR, RETENTION_DAYS, BACKUP_TIME)
