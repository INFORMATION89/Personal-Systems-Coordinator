#!/usr/bin/env python3
"""Pull-request hygiene checks for Personal Systems Coordinator (adapted from Meridian-Engine).

Enforces two rules from RULES.md section 12:

1. No commit that changes non-documentation files may carry a CI-skip marker,
   because that code would never run through the platform matrix.
2. The PR description must fill in the required template sections.

Usage: pr_hygiene.py <base-sha> <head-sha>
The PR description is read from the PR_BODY environment variable (never
interpolated into a shell command).
"""

import os
import re
import subprocess
import sys

SKIP_MARKERS = re.compile(
    r"\[(skip ci|ci skip|no ci|skip actions|actions skip)\]|skip-checks:\s*true",
    re.IGNORECASE,
)

REQUIRED_SECTIONS = [
    "Tool and tier",
    "Task",
    "Sources consulted",
    "Checks run",
    "Not run",
]


def is_documentation(path: str) -> bool:
    return (
        path.endswith(".md")
        or path.startswith("docs/")
        or path.startswith("wiki/")
        or path == "LICENSE"
    )


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], check=True, capture_output=True, text=True
    ).stdout


def check_skip_ci(base: str, head: str) -> list[str]:
    errors = []
    for sha in git("rev-list", "--no-merges", f"{base}..{head}").split():
        message = git("log", "-1", "--format=%B", sha)
        if not SKIP_MARKERS.search(message):
            continue
        files = git("diff-tree", "--no-commit-id", "--name-only", "-r", sha).split()
        code = [f for f in files if not is_documentation(f)]
        if code:
            subject = message.splitlines()[0] if message else ""
            errors.append(
                f"Commit {sha[:10]} ('{subject}') skips CI but changes "
                f"non-documentation files: {', '.join(code[:5])}"
            )
    return errors


def check_body(body: str) -> list[str]:
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    sections: dict[str, str] = {}
    current = None
    for line in body.splitlines():
        heading = re.match(r"^#{2,3}\s+(.+?)\s*$", line)
        if heading:
            current = heading.group(1).strip().lower()
            sections.setdefault(current, "")
        elif current is not None:
            sections[current] += line.strip()
    errors = []
    for name in REQUIRED_SECTIONS:
        content = sections.get(name.lower())
        if content is None:
            errors.append(f"PR description is missing the '## {name}' section.")
        elif not content:
            errors.append(f"PR description section '## {name}' is empty.")
    return errors


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    base, head = sys.argv[1], sys.argv[2]
    errors = check_skip_ci(base, head) + check_body(os.environ.get("PR_BODY", ""))
    for error in errors:
        print(f"::error::{error}")
    if errors:
        print(
            "See .github/pull_request_template.md and "
            "RULES.md section 12."
        )
        return 1
    print("PR hygiene checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
