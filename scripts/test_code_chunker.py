from app.ingestion.code_chunker import CodeChunker

code = """
class A:
    def foo(self):
        pass

def bar():
    return 1
"""

chunker = CodeChunker()

for chunk in chunker.chunk(code):
    print(chunk)
    print("-" * 30)