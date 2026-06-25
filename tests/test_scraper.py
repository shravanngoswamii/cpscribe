from cpscribe.scraper import extract_url_from_cpp, parse_url


def test_parse_contest_url():
    cid, idx = parse_url("https://codeforces.com/contest/1594/problem/A")
    assert (cid, idx) == ("1594", "A")


def test_parse_problemset_url():
    cid, idx = parse_url("https://codeforces.com/problemset/problem/1903/B")
    assert (cid, idx) == ("1903", "B")


def test_extract_url_from_line_comment():
    code = "// https://codeforces.com/contest/1594/problem/A\nint main(){}"
    assert extract_url_from_cpp(code) == "https://codeforces.com/contest/1594/problem/A"


def test_extract_url_from_block_comment():
    code = "/* https://codeforces.com/problemset/problem/1903/B */\nint main(){}"
    assert extract_url_from_cpp(code) == "https://codeforces.com/problemset/problem/1903/B"


def test_extract_url_missing():
    assert extract_url_from_cpp("#include <bits/stdc++.h>\nint main(){}") is None
