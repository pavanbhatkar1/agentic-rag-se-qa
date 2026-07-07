from pathlib import Path
from app.ingestion.markdown_parser import MarkdownParser

parser = MarkdownParser()

text = parser.parse(
    Path("data/raw/repos/fastapi/README.md")
)

print(text[:500])
