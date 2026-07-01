import re
from datetime import datetime, timezone


def _slug(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-")


def _title(slug: str) -> str:
    return " ".join(w.capitalize() for w in slug.split("-"))


def _fmt_examples(samples: list[tuple[str, str]]) -> str:
    if not samples:
        return "<!-- paste sample inputs/outputs here -->"
    parts = []
    for i, (inp, out) in enumerate(samples, 1):
        label = f"**Example {i}**" if len(samples) > 1 else "**Example**"
        parts.append(f"{label}\n\nInput:\n```\n{inp}\n```\nOutput:\n```\n{out}\n```")
    return "\n\n".join(parts)


def build(
    contest_id: str,
    index: str,
    problem: dict,
    cpp_code: str,
    author: str,
    platform: str = "codeforces",
    section: str | None = None,
) -> str:
    name = problem["name"]
    rating = problem["rating"]
    contest = problem["contest"]
    note_block = f"\n\n### Note\n\n{problem['note']}" if problem.get("note") else ""
    pub_dt = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    cf_url = problem.get("url") or f"https://codeforces.com/problemset/problem/{contest_id}/{index}"

    slug_section = section or contest_id
    slug = f"cp/{platform}/{slug_section}/{index}"

    if platform == "codeforces" and not section:
        title = f"{index}. {name} (CF{contest_id} {rating} RATED)"
        tags = f"[CPP, Codeforces, CF{rating}]"
        description = f"{index}. {name}, {rating} RATED - {contest}"
        aliases = f"\naliases:\n  - /writing/{contest_id}-{index}-{_slug(name)}"
    else:
        title = name
        tags = f"[CPP, {_title(platform)}]"
        description = f"{name} — {contest}"
        aliases = ""

    return f"""\
---
author: {author}
pubDatetime: {pub_dt}
title: "{title}"
slug: {slug}
tags: {tags}
description: "{description}"{aliases}
---

Problem Link: [{index}. {name}, {rating} RATED - {contest}]({cf_url})

| Time Limit | Memory Limit |
| --- | --- |
| {problem["time_lim"]} | {problem["mem_lim"]} |

## Problem Statement

{problem["body"]}

### Input

{problem["input_spec"]}

### Output

{problem["output_spec"]}{note_block}

## Examples

{_fmt_examples(problem["samples"])}

## My Understanding

<!-- How do you model or restate this problem in your own words? -->

## Key Observations

- <!-- Observation 1 -->
- <!-- Observation 2 -->

## Approach

<!-- Walk through your full solution strategy -->

## Complexity

- **Time:** $O()$
- **Space:** $O()$

## Solution

```cpp
{cpp_code}
```

## What I Learned

<!-- Key takeaway, trick, or pattern from this problem -->
"""
