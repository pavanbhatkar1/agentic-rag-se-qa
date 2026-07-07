from copy import deepcopy


class Chunker:
    """Split documents into overlapping chunks."""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, documents: list[dict]) -> list[dict]:
        chunks = []

        for document in documents:
            text = document["content"]

            start = 0
            chunk_id = 0

            while start < len(text):
                end = start + self.chunk_size
                chunk_text = text[start:end].strip()

                if chunk_text:
                    metadata = deepcopy(document["metadata"])
                    metadata["chunk_id"] = chunk_id

                    chunks.append(
                        {
                            "content": chunk_text,
                            "metadata": metadata,
                        }
                    )

                start += self.chunk_size - self.chunk_overlap
                chunk_id += 1

        return chunks
    