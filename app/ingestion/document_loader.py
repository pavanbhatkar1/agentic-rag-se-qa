from pathlib import Path

from app.ingestion.chunker import Chunker
from app.ingestion.code_chunker import CodeChunker
from app.ingestion.code_parser import CodeParser
from app.ingestion.markdown_parser import MarkdownParser


class DocumentLoader:
    def __init__(self):
        self.markdown_parser = MarkdownParser()
        self.code_parser = CodeParser()
        self.chunker = Chunker()
        self.code_chunker = CodeChunker()

    def load(self, files: list[Path]) -> list[dict]:
        documents = []

        for file_path in files:
            suffix = file_path.suffix.lower()

            if suffix in {".md", ".mdx"}:
                content = self.markdown_parser.parse(file_path)
                chunks = [
                    c["content"]
                    for c in self.chunker.chunk(
                        [{
                            "content": content,
                            "metadata": {},
                        }]
                    )
                ]

            else:
                content = self.code_parser.parse(file_path)

                if suffix == ".py":
                    chunks = self.code_chunker.chunk(content)
                else:
                    chunks = [
                        c["content"]
                        for c in self.chunker.chunk(
                            [{
                                "content": content,
                                "metadata": {},
                            }]
                        )
                    ]

            for i, chunk in enumerate(chunks):
                if not chunk.strip():
                    continue

                documents.append(
                    {
                        "content": chunk,
                        "metadata": {
                            "source": str(file_path),
                            "file_type": suffix,
                            "chunk_id": i,
                        },
                    }
                )

        return documents