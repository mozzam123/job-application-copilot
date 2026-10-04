import sys
from pathlib import Path

import httpx


ROOT_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(ROOT_DIR))


from app.knowledge.project_index import ProjectIndex
from app.knowledge.project_sources import (
    GITHUB_USERNAME,
    PROJECT_REPOSITORIES,
)


def fetch_readme(
    username: str,
    repository: str,
) -> str | None:

    branches = [
        "main",
        "master",
    ]

    for branch in branches:

        url = (
            f"https://raw.githubusercontent.com/"
            f"{username}/"
            f"{repository}/"
            f"{branch}/README.md"
        )

        try:
            response = httpx.get(
                url,
                timeout=20.0,
                follow_redirects=True,
            )

            if response.status_code == 200:
                return response.text

        except httpx.HTTPError as exc:
            print(f"Error reading {repository}: {exc}")

    return None


def main():

    projects = []

    print("\nFetching GitHub projects...\n")

    for repository in PROJECT_REPOSITORIES:

        readme = fetch_readme(
            GITHUB_USERNAME,
            repository,
        )

        if not readme:
            print(f"Skipped: {repository} " "(README not found)")

            continue

        project_url = f"https://github.com/" f"{GITHUB_USERNAME}/" f"{repository}"

        content = f"""
Project: {repository}

GitHub:
{project_url}

README:
{readme}
""".strip()

        projects.append(
            {
                "repository": repository,
                "url": project_url,
                "content": content,
            }
        )

        print(f"Fetched: {repository}")

    if not projects:
        print("\nNo projects were found.")
        return

    print(f"\nCreating embeddings for " f"{len(projects)} projects...\n")

    project_index = ProjectIndex()

    project_index.add_projects(projects)

    project_index.save()

    print("\nProject knowledge base created.")


if __name__ == "__main__":
    main()
