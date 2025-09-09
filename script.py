import os
import re
import subprocess
from pathlib import Path

# === CONFIGURATION ===
repo_urls = [
    "https://github.com/AkshatJMe/LearnPulse.git",
    "https://github.com/AkshatJMe/TicTacToe.git",
    "https://github.com/AkshatJMe/BookNest.git",
    "https://github.com/AkshatJMe/WeatherApp.git",
    "https://github.com/AkshatJMe/DesignPatterns.git",
    "https://github.com/AkshatJMe/TravelEase.git",
    "https://github.com/AkshatJMe/ECommerce.git",
]

old_username = "HiAkshatJain"
new_username = "AkshatJMe"
base_dir = "cloned_repos"
commit_message = f"Fix image URLs: replace {old_username} with {new_username}"
push_changes = True  # Set to False if you don't want to push


# === FUNCTIONS ===

def run_cmd(cmd, cwd=None):
    print(f"\n$ {' '.join(cmd)} (in {cwd})")
    subprocess.run(cmd, cwd=cwd, check=True)


def clone_repo(url, base_dir):
    os.makedirs(base_dir, exist_ok=True)
    repo_name = url.rstrip('/').split('/')[-1].replace('.git', '')
    repo_path = os.path.join(base_dir, repo_name)
    if os.path.exists(repo_path):
        print(f"[SKIP] Already cloned: {repo_name}")
        return repo_path
    print(f"[CLONE] Cloning {url}...")
    run_cmd(["git", "clone", url], cwd=base_dir)
    return repo_path


def update_readme_files(repo_path, old_username, new_username):
    changed_files = []
    for readme in Path(repo_path).rglob("README.md"):
        with open(readme, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = re.sub(
            rf"(https://github\.com/){old_username}(/[^)\s]+)",
            rf"\1{new_username}\2",
            content
        )

        if new_content != content:
            with open(readme, "w", encoding="utf-8") as f:
                f.write(new_content)
            changed_files.append(str(readme.relative_to(repo_path)))
            print(f"[MODIFIED] {readme}")
    return changed_files


def commit_and_push(repo_path, changed_files):
    if not changed_files:
        print("[NO CHANGES] No README files were updated.")
        return
    print(f"[GIT] Committing changes in {repo_path}")
    run_cmd(["git", "add", "."], cwd=repo_path)
    run_cmd(["git", "commit", "-m", commit_message], cwd=repo_path)
    if push_changes:
        print(f"[GIT] Pushing changes...")
        run_cmd(["git", "push"], cwd=repo_path)


# === MAIN ===

def main():
    for url in repo_urls:
        repo_path = clone_repo(url, base_dir)
        changed_files = update_readme_files(repo_path, old_username, new_username)
        commit_and_push(repo_path, changed_files)


if __name__ == "__main__":
    main()
