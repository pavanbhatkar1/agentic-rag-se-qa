from pathlib import Path

from app.ingestion.code_parser import CodeParser
from app.ingestion.markdown_parser import MarkdownParser


class DocumentLoader:
    """Load and parse repository files."""

    def __init__(self):
        self.markdown_parser = MarkdownParser()
        self.code_parser = CodeParser()

    def load(self, files: list[Path]) -> list[dict]:
        documents = []

        for file_path in files:
            if file_path.suffix.lower() in {".md", ".mdx"}:
                content = self.markdown_parser.parse(file_path)
            else:
                content = self.code_parser.parse(file_path)

            if not content:
                continue

            documents.append(
                {
                    "content": content,
                    "metadata": {
                        "source": str(file_path),
                        "file_type": file_path.suffix.lower(),
                    },
                }
            )

        return documents
    