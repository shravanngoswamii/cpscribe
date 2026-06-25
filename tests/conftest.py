import pytest


@pytest.fixture
def problem() -> dict:
    return {
        "name": "Consecutive Sum Riddle",
        "rating": "800",
        "contest": "Codeforces Round 747 (Div. 2)",
        "time_lim": "2 seconds",
        "mem_lim": "256 megabytes",
        "body": "Find $l$ and $r$ such that $l + \\ldots + r = n$.\n\n",
        "input_spec": "A single integer $n$ ($1 \\le n \\le 10^{12}$).\n\n",
        "output_spec": "Print two integers $l$ and $r$.\n\n",
        "note": "",
        "samples": [("3\n4\n5", "1 2\n1 3\n2 3")],
    }
