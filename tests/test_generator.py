from cpscribe import generator


def test_frontmatter(problem):
    md = generator.build("1594", "A", problem, "// code", "Test Author")
    assert "pubDatetime:" in md
    assert 'title: "A. Consecutive Sum Riddle (CF1594 800 RATED)"' in md
    assert "slug: cp/codeforces/1594/A" in md
    assert "tags: [CPP, Codeforces, CF800]" in md


def test_single_alias(problem):
    md = generator.build("1594", "A", problem, "", "Test Author")
    assert md.count("  - /") == 1
    assert "/writing/1594-A-Consecutive-Sum-Riddle" in md


def test_sections_present(problem):
    md = generator.build("1594", "A", problem, "", "Test Author")
    for section in ("## Problem Statement", "## Examples", "## Approach", "## Solution", "## What I Learned"):
        assert section in md


def test_solution_code_injected(problem):
    code = "#include <bits/stdc++.h>\nint main(){}"
    assert code in generator.build("1594", "A", problem, code, "Test Author")


def test_note_omitted_when_empty(problem):
    problem["note"] = ""
    assert "### Note" not in generator.build("1594", "A", problem, "", "Test Author")


def test_note_included_when_present(problem):
    problem["note"] = "Constraints are tight."
    assert "### Note" in generator.build("1594", "A", problem, "", "Test Author")
