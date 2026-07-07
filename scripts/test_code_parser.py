from pathlib import Path

from app.ingestion.code_parser import CodeParser

parser = CodeParser()

text = parser.parse(Path("main.py"))

print(text[:500])
