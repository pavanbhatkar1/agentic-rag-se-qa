from __future__ import annotations

import logging
from pathlib import Path
from urllib.parse import urlparse

from git import GitCommandError, Repo

logger = logging.getLogger(__name__)


class GitHubLoader:
    """Clone and update GitHub repositories."""

    def __init__(self, base_dir: str | Path = "data/raw/repos") -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def clone_or_update(self, repo_url: str) -> Path:
        """
        Clone a GitHub repository if it does not exist.
        Otherwise, pull the latest changes.

        Args:
            repo_url: GitHub repository URL.

        Returns:
            Local path to the repository.

        Raises:
            ValueError: If the URL is invalid.
            RuntimeError: If clone/pull fails.
        """
        repo_name = self._get_repo_name(repo_url)
        repo_path = self.base_dir / repo_name

        try:
            if repo_path.exists():
                logger.info("Updating repository: %s", repo_name)

                repo = Repo(repo_path)
                repo.remotes.origin.pull()

                logger.info("Repository updated successfully.")
            else:
                logger.info("Cloning repository: %s", repo_name)

                Repo.clone_from(repo_url, repo_path)

                logger.info("Repository cloned successfully.")

            return repo_path

        except GitCommandError as exc:
            logger.exception("Git operation failed.")
            raise RuntimeError(f"Failed to process repository: {repo_url}") from exc

    @staticmethod
    def _get_repo_name(repo_url: str) -> str:
        """
        Extract repository name from a GitHub URL.

        Example:
            https://github.com/fastapi/fastapi.git
            -> fastapi
        """
        parsed = urlparse(repo_url)

        if parsed.netloc != "github.com":
            raise ValueError("Only GitHub repositories are supported.")

        repo_name = Path(parsed.path).stem

        if not repo_name:
            raise ValueError("Invalid GitHub repository URL.")

        return repo_name