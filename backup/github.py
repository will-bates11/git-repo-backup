import requests
import logging

def fetch_github_repos(username, token, include_private):
    headers = {"Authorization": f"token {token}"} if token else {}
    repos = []
    page = 1
    per_page = 100
    while True:
        if include_private:
            url = f"https://api.github.com/user/repos?per_page={per_page}&page={page}&affiliation=owner"
        else:
            url = f"https://api.github.com/users/{username}/repos?per_page={per_page}&page={page}&type=owner"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            logging.error(f"GitHub API error ({url}): {resp.text}")
            break
        rs = resp.json()
        if not rs: break
        for r in rs:
            if r['owner']['login'].lower() != username.lower():
                continue
            repos.append({
                "name": r["name"],
                "clone_url": r["ssh_url"] if token else r["clone_url"]
            })
        if len(rs) < per_page: break
        page += 1
    return repos