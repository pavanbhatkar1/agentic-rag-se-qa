from pathlib import Path


class CodeParser:
    """Read source code files."""

    def parse(self, file_path: Path) -> str:
        try:
            return file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            ).strip()
        except Exception:
            return ""
        