from pathlib import Path


SUPPORTED_EXTENSIONS = {".md", ".py"}

IGNORED_DIRS = {
    ".git",
    ".github",
    "__pycache__",
    "venv",
    ".venv",
    "node_modules",
    "build",
    "dist",
}


class FileScanner:
    """Scan a repository for supported files."""

    def scan(self, repo_path: str | Path) -> list[Path]:
        repo_path = Path(repo_path)

        files = []

        for file_path in repo_path.rglob("*"):
            if not file_path.is_file():
                continue

            if any(part in IGNORED_DIRS for part in file_path.parts):
                continue

            if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            files.append(file_path)

        return sorted(files)