import re
from typing import List, Tuple

class CustomMarkdownParser:
    def __init__(self):
        # Define regex patterns for different markdown elements
        self.patterns = {
            'bold_italic': r'\*\*\*(.*?)\*\*\*',  # ***text***
            'bold': r'\*\*(.*?)\*\*',             # **text**
            'italic': r'\*(.*?)\*',               # *text*
            'heading': r'^(#{1,6})\s+(.+)$',      # # Heading
            'bullet_point': r'^\s*[-*+]\s+(.+)$'  # - item or * item or + item
        }

    def parse(self, text: str) -> Tuple[str, List[Tuple[str, int, int]]]:
        """
        Parse markdown text and return plain text with tag information
        Returns:
            Tuple containing:
            - Plain text with markdown removed
            - List of tuples (tag_name, start_index, end_index)
        """
        if not text:
            return "", []

        # Split text into lines for processing
        lines = text.split('\n')
        plain_lines = []
        tags = []
        current_pos = 0

        for line in lines:
            # Process other markdown elements
            plain_line, line_tags = self._process_line(line, current_pos)
            plain_lines.append(plain_line)
            tags.extend(line_tags)
            current_pos += len(plain_line) + 1  # +1 for newline

        return '\n'.join(plain_lines), tags

    def _process_line(self, line: str, start_pos: int) -> Tuple[str, List[Tuple[str, int, int]]]:
        """Process a single line of markdown text"""
        plain_text = line
        tags = []
        current_pos = 0

        # Process headings
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if heading_match:
            level = len(heading_match.group(1))
            content = heading_match.group(2)
            plain_text = content
            tags.append((f'heading{level}', start_pos, start_pos + len(content)))
            return plain_text, tags

        # Process bullet points
        bullet_match = re.match(self.patterns['bullet_point'], line)
        if bullet_match:
            content = bullet_match.group(1)
            plain_text = "• " + content  # Add round bullet point
            tags.append(('bullet', start_pos, start_pos + len(plain_text)))
            # Process inline formatting within bullet point
            inline_text, inline_tags = self._process_inline_formatting(content, start_pos + 2)  # +2 for "• "
            tags.extend(inline_tags)
            return plain_text, tags

        # Process inline formatting
        return self._process_inline_formatting(line, start_pos)

    def _process_inline_formatting(self, text: str, start_pos: int) -> Tuple[str, List[Tuple[str, int, int]]]:
        """Process all inline formatting (bold, italic)"""
        tags = []
        plain_text = text
        offset = 0

        # Process bold and italic (***text***)
        for match in re.finditer(self.patterns['bold_italic'], plain_text):
            start, end = match.span()
            content = match.group(1)
            plain_text = plain_text[:start] + content + plain_text[end:]
            tags.append(('bold_italic', start_pos + start, start_pos + start + len(content)))
            offset += 4  # Account for removed asterisks

        # Process bold (**text**)
        for match in re.finditer(self.patterns['bold'], plain_text):
            start, end = match.span()
            content = match.group(1)
            plain_text = plain_text[:start] + content + plain_text[end:]
            tags.append(('bold', start_pos + start, start_pos + start + len(content)))
            offset += 2  # Account for removed asterisks

        # Process italic (*text*)
        for match in re.finditer(self.patterns['italic'], plain_text):
            start, end = match.span()
            content = match.group(1)
            plain_text = plain_text[:start] + content + plain_text[end:]
            tags.append(('italic', start_pos + start, start_pos + start + len(content)))
            offset += 2  # Account for removed asterisks

        return plain_text, tags 