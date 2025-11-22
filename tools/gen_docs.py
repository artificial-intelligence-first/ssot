"""
Generate virtual documentation pages from repository root sources for MkDocs.
This keeps `docs/` free of wrapper files while still exposing root Markdown.
"""

from pathlib import Path

import mkdocs_gen_files

ROOT = Path(__file__).resolve().parent.parent

SOURCES = {
    "index.md": ROOT / "README.md",
    "AGENTS.md": ROOT / "AGENTS.md",
    "_templates/TOPIC_TEMPLATE.md": ROOT / "_templates/TOPIC_TEMPLATE.md",
    "_templates/SECTION_TEMPLATE.md": ROOT / "_templates/SECTION_TEMPLATE.md",
    "_templates/FRONT_MATTER.md": ROOT / "_templates/FRONT_MATTER.md",
}

def rewrite_links(name: str, content: str) -> str:
    """Adjust intra-repo relative links to match MkDocs output paths."""
    if name == "index.md":
        content = content.replace("./docs/", "")
        content = content.replace("./_templates/", "_templates/")
        content = content.replace("./LICENSE", "https://github.com/artificial-intelligence-first/ssot/blob/main/LICENSE")
    if name == "AGENTS.md":
        content = content.replace("./docs/", "")
    return content

for target, source in SOURCES.items():
    text = source.read_text(encoding="utf-8")
    text = rewrite_links(target, text)
    with mkdocs_gen_files.open(target, "w") as dest:
        dest.write(text)
