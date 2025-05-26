#!/usr/bin/env python3
import logging
from backup.config import load_config
from backup.github import fetch_github_repos
from backup.gitlab import fetch_gitlab_repos
from backup.backup_manager import backup_repo
import os

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler("backup.log"),
            logging.StreamHandler()
        ]
    )

def main():
    setup_logging()
    config = load_config("config.yaml")
    backup_dir = config["backup_dir"]
    retention = config.get("retention_count", 7)

    for src in config["sources"]:
        typ = src["type"].lower()
        user = src["username"]
        token = src.get("token")
        include_private = src.get("include_private", False)
        src_dir = os.path.join(backup_dir, f"{typ}_{user}")
        os.makedirs(src_dir, exist_ok=True)
        if typ == "github":
            repos = fetch_github_repos(user, token, include_private)
        elif typ == "gitlab":
            gitlab_url = src.get("gitlab_url", "https://gitlab.com")
            repos = fetch_gitlab_repos(user, token, include_private, gitlab_url)
        else:
            logging.warning(f"Unknown source type: {typ}")
            continue
        for repo in repos:
            backup_repo(repo, src_dir, retention)

if __name__ == "__main__":
    main()