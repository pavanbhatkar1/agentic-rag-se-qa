from pathlib import Path
import re


class MarkdownParser:
    """Parse Markdown files into clean plain text."""

    CODE_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)
    INLINE_CODE_RE = re.compile(r"`[^`]*`")
    LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
    IMAGE_RE = re.compile(r"!\[[^\]]*]\([^)]+\)")
    EMPHASIS_RE = re.compile(r"(\*\*|\*|__|_)")
    HEADER_RE = re.compile(r"^#{1,6}\s*", re.MULTILINE)
    BLOCKQUOTE_RE = re.compile(r"^>\s?", re.MULTILINE)
    LIST_RE = re.compile(r"^[-*+]\s+", re.MULTILINE)

    def parse(self, file_path: Path) -> str:
        text = file_path.read_text(encoding="utf-8", errors="ignore")

        text = self.CODE_BLOCK_RE.sub("", text)
        text = self.INLINE_CODE_RE.sub("", text)
        text = self.IMAGE_RE.sub("", text)
        text = self.LINK_RE.sub(r"\1", text)
        text = self.EMPHASIS_RE.sub("", text)
        text = self.HEADER_RE.sub("", text)
        text = self.BLOCKQUOTE_RE.sub("", text)
        text = self.LIST_RE.sub("", text)

        # Remove horizontal rules
        text = re.sub(r"^---+$", "", text, flags=re.MULTILINE)

        # Collapse whitespace
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]+", " ", text)

        return text.strip()