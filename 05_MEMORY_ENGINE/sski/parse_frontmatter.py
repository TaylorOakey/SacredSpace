import re
import yaml

def parse_note(content: str):
    """Extract YAML frontmatter and return (metadata, body)."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", content, re.DOTALL)
    if not match:
        return {}, content

    try:
        data = yaml.safe_load(match.group(1))
        body = content[match.end():]
        return (data if isinstance(data, dict) else {}), body
    except Exception:
        return {}, content
