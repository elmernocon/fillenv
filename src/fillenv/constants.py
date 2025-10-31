# Copyright (c) 2025 Elmer Nocon
# SPDX-License-Identifier: MIT

from typing import Tuple

# Keys whose values should be masked during interactive prompts.
# The match is case-insensitive and based on substring membership.
SENSITIVE_HINTS: Tuple[str, ...] = ("KEY", "PASSWORD", "SECRET", "TOKEN")
