from app.core.logging import setup_logging
from app.ingestion.github_loader import GitHubLoader

setup_logging()

loader = GitHubLoader()

path = loader.clone_or_update(
    "https://github.com/fastapi/fastapi.git"
)

print(path)