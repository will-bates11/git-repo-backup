# Git Repo Backup Automation

Backup all your GitHub and GitLab repositories, public and private, on a schedule, with retention, logging, and easy config.

## Features

- **Supports both GitHub & GitLab (including self-hosted)**
- **Backs up all public/private repos with API tokens**
- **Per-repo timestamped, mirror backups (`git clone --mirror`)**
- **Retention policy: auto-removes old backups**
- **Detailed logs for audit**
- **YAML config (edit in one place)**
- **One-step cron integration**
- **No dependencies beyond Python3, `requests`, `PyYAML`, and `git`**

## Quickstart

### 1. Clone & Install

```bash
git clone https://github.com/will-bates11/git-repo-backup-automation.git
cd git-repo-backup-automation
pip install -r requirements.txt
```

### 2. Edit the Config

- Copy `config.yaml`
- Add your GitHub/GitLab usernames or orgs, and API tokens (see below)
- Set the `backup_dir` to your desired local path

### 3. Run

```bash
python3 backup_repos.py
```

### 4. Automate with Cron

Run `crontab -e` and add:

```bash
0 3 * * * cd /full/path/to/git-repo-backup-automation && /usr/bin/python3 backup_repos.py
```

This will back up every day at 3AM.



## Example config.yaml

```yaml
backup_dir: "/home/wbat/backups/git"
retention_count: 5

sources:
  - type: github
    username: will-bates11
    token: "${GITHUB_TOKEN}"
    include_private: true

  - type: gitlab
    username: mygitlaborg
    token: "${GITLAB_TOKEN}"
    include_private: true
    gitlab_url: "https://gitlab.com"
```


## Security

- Store tokens securely. Use environment variables or a secrets manager.
- Backups are plain git `--mirror` repositories—no code execution risk, but secure your storage.

## Troubleshooting

- **Permission errors?** Ensure tokens have read access to all repos.
- **Backups not created?** Check `backup.log` for error details.

## License

MIT (see LICENSE)