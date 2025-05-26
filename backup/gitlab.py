import requests
import logging

def fetch_gitlab_repos(username, token, include_private, gitlab_url):
    headers = {"PRIVATE-TOKEN": token} if token else {}
    projects = []
    page = 1
    per_page = 100
    tried_group = False
    while True:
        if not tried_group:
            url = f"{gitlab_url}/api/v4/users/{username}/projects?per_page={per_page}&page={page}"
        else:
            url = f"{gitlab_url}/api/v4/groups/{username}/projects?per_page={per_page}&page={page}"
        resp = requests.get(url, headers=headers)
        if resp.status_code == 404 and not tried_group and page == 1:
            tried_group = True
            page = 1
            continue
        if resp.status_code != 200:
            logging.error(f"GitLab API error ({url}): {resp.text}")
            break
        rs = resp.json()
        if not rs: break
        for r in rs:
            if include_private or r.get("visibility") == "public":
                projects.append({
                    "name": r["name"],
                    "clone_url": r["ssh_url_to_repo"] if token else r["http_url_to_repo"]
                })
        if len(rs) < per_page: break
        page += 1
    return projects