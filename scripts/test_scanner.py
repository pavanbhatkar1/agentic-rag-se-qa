from app.ingestion.file_scanner import FileScanner

scanner = FileScanner()

files = scanner.scan("data/raw/repos/fastapi")

print(f"Found {len(files)} files\n")

for file in files[:20]:
    print(file)
    