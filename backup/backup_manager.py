import os
import subprocess
import datetime
import logging
import shutil
import re

def backup_repo(repo, backup_dir, retention):
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    name = repo["name"]
    clone_url = repo["clone_url"]
    backup_name = f"{name}_{ts}.git"
    backup_path = os.path.join(backup_dir, backup_name)

    logging.info(f"Backing up '{name}' to '{backup_path}' ...")
    try:
        subprocess.run(
            ["git", "clone", "--mirror", clone_url, backup_path],
            check=True, timeout=600
        )
        # Retention: keep last N
        backups = sorted(
            [d for d in os.listdir(backup_dir) if re.match(rf"^{re.escape(name)}_\d+T\d+Z\.git$", d)],
            reverse=True
        )
        if len(backups) > retention:
            for old in backups[retention:]:
                old_path = os.path.join(backup_dir, old)
                logging.info(f"Removing old backup: {old_path}")
                shutil.rmtree(old_path, ignore_errors=True)
    except Exception as e:
        logging.error(f"Failed to backup {name}: {e}")