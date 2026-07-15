import ast


class CodeChunker:
    """AST-aware chunker for Python code."""

    def chunk(self, code: str) -> list[str]:
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return [code]

        chunks = []

        for node in tree.body:
            if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef),
            ):
                chunks.append(ast.unparse(node))

        return chunks if chunks else [code]