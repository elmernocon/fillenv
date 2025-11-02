# Copyright (c) 2025 Elmer Nocon
# SPDX-License-Identifier: MIT

import argparse
import os
import sys
from typing import List, Optional

from .parser import parse_template_lines
from .prompt import prompt_for_values
from .serialize import serialize_value


def run(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Fill values for variables from a .env.template "
            "and write KEY=value lines to output file (default: .env, "
            "or .env1, .env2, ... if file exists and --overwrite is not set)."
        )
    )
    parser.add_argument(
        "template",
        nargs="?",
        default=".env.template",
        help="Path to the env template file (default: .env.template)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing output file if it exists",
    )
    parser.add_argument(
        "--output",
        default=".env",
        help="Path to the output env file (default: .env)",
    )
    args = parser.parse_args(argv)

    template_path: str = args.template
    if not os.path.exists(template_path):
        print(f"Error: template file not found: {template_path}", file=sys.stderr)
        return 2

    lines: List[str] = []
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error: failed to read template: {e}", file=sys.stderr)
        return 2

    entries = parse_template_lines(lines)
    if not entries:
        return 0

    filled = prompt_for_values(entries)

    # Choose output filename: use --output value, or append 1, 2, ... if existing
    if args.overwrite:
        out_path = args.output
    else:
        counter = 0
        base_name = args.output
        out_path = base_name
        while os.path.exists(out_path):
            counter += 1
            out_path = f"{base_name}{counter}"

    try:
        with open(out_path, "w", encoding="utf-8") as outf:
            for key, value in filled:
                outf.write(f"{key}={serialize_value(value)}\n")
    except Exception as e:
        print(f"Error: failed to write env file: {e}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(run())
