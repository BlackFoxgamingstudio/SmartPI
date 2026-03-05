#!/usr/bin/env python3
"""Sync handbook_chatbot.csv into the embedded <script id="handbook-csv"> block in index.html.

Run from repo root after editing handbook_chatbot.csv so file:// and fallback use the same Q&A.
"""

import re
from pathlib import Path


def main() -> None:
    repo = Path(__file__).resolve().parent.parent
    csv_path = repo / "handbook_chatbot.csv"
    index_path = repo / "index.html"

    if not csv_path.exists():
        raise SystemExit(f"Missing {csv_path}")
    if not index_path.exists():
        raise SystemExit(f"Missing {index_path}")

    csv_content = csv_path.read_text(encoding="utf-8")
    # Ensure single trailing newline so embedded block is clean
    csv_content = csv_content.rstrip("\n") + "\n"

    html = index_path.read_text(encoding="utf-8")

    # Pattern: from opening tag (with possible newline/space) to closing </script>
    open_tag = '<script type="text/plain" id="handbook-csv">'
    close_tag = "</script>"
    # Match open_tag, then any content (non-greedy), then close_tag
    pattern = re.compile(
        re.escape(open_tag) + r"\n?(.*?)" + re.escape(close_tag),
        re.DOTALL,
    )
    replacement = open_tag + "\n" + csv_content + "  " + close_tag
    new_html, n = pattern.subn(replacement, html, count=1)
    if n != 1:
        raise SystemExit("Could not find exactly one handbook-csv script block in index.html")
    index_path.write_text(new_html, encoding="utf-8")
    line_count = len(csv_content.strip().splitlines())
    print(f"Synced {csv_path.name} ({line_count} lines) into index.html embedded block.")


if __name__ == "__main__":
    main()
