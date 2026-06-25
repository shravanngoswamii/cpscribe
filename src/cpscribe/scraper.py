import re
import sys

import cloudscraper
from bs4 import BeautifulSoup, NavigableString

CF_URL_RE = re.compile(
    r"https://codeforces\.com/(?:contest|problemset/problem)/\d+/(?:problem/)?[A-Za-z]\d*"
)


def parse_url(url: str) -> tuple[str, str]:
    m = re.search(r"/(?:contest|problemset/problem)/(\d+)/(?:problem/)?([A-Za-z]\d*)", url)
    if not m:
        sys.exit(f"could not parse URL: {url}")
    return m.group(1), m.group(2).upper()


def extract_url_from_cpp(text: str) -> str | None:
    m = CF_URL_RE.search(text)
    return m.group(0) if m else None


def _fix_math(text: str) -> str:
    return re.sub(r"\$\$\$(.+?)\$\$\$", r"$\1$", text, flags=re.DOTALL)


def _node_to_md(node) -> str:
    if isinstance(node, NavigableString):
        return _fix_math(str(node))
    tag = node.name
    inner = "".join(_node_to_md(c) for c in node.children)
    match tag:
        case "p":
            return inner.strip() + "\n\n"
        case "strong" | "b":
            return f"**{inner}**"
        case "em" | "i":
            return f"*{inner}*"
        case "ul" | "ol":
            return inner
        case "li":
            return f"- {inner.strip()}\n"
        case "br":
            return "\n"
        case "div" if "section-title" in node.get("class", []):
            return ""
        case _:
            return inner


def _section_md(div) -> str:
    if not div:
        return ""
    return "".join(_node_to_md(c) for c in div.children).strip()


def _sample_pre(div) -> str:
    pre = div.find("pre")
    if not pre:
        return ""
    lines = pre.find_all("div", class_="test-example-line")
    if lines:
        return "\n".join(d.get_text() for d in lines).strip()
    for br in pre.find_all("br"):
        br.replace_with("\n")
    return pre.get_text().strip()


def scrape(contest_id: str, index: str) -> dict:
    url = f"https://codeforces.com/problemset/problem/{contest_id}/{index}"
    resp = cloudscraper.create_scraper().get(url, timeout=15)
    if resp.status_code != 200:
        sys.exit(f"problem page returned {resp.status_code}")

    soup = BeautifulSoup(resp.content, "html.parser")
    ps = soup.find("div", class_="problem-statement")

    header = ps.find("div", class_="header")
    title_div = header.find("div", class_="title") if header else None
    name = re.sub(r"^[A-Z]\d*\.\s*", "", title_div.text.strip()) if title_div else "Unknown"

    rating_tag = soup.find("span", class_="tag-box", title="Difficulty")
    rating = rating_tag.text.strip().replace("*", "") if rating_tag else "Unrated"

    rtable = soup.find("table", class_="rtable")
    link = rtable.find("a") if rtable else None
    contest = link.text.strip() if link else f"Codeforces Contest {contest_id}"

    time_tag = soup.find("div", class_="time-limit")
    mem_tag = soup.find("div", class_="memory-limit")
    time_lim = time_tag.text.replace("time limit per test", "").strip() if time_tag else "2 seconds"
    mem_lim = (
        mem_tag.text.replace("memory limit per test", "").strip() if mem_tag else "256 megabytes"
    )

    body_div = next((c for c in ps.children if hasattr(c, "get") and not c.get("class")), None)

    samples = []
    for block in soup.find_all("div", class_="sample-test"):
        for inp_div, out_div in zip(
            block.find_all("div", class_="input"),
            block.find_all("div", class_="output"),
        ):
            samples.append((_sample_pre(inp_div), _sample_pre(out_div)))

    return {
        "name": name,
        "rating": rating,
        "contest": contest,
        "time_lim": time_lim,
        "mem_lim": mem_lim,
        "body": _section_md(body_div),
        "input_spec": _section_md(ps.find("div", class_="input-specification")),
        "output_spec": _section_md(ps.find("div", class_="output-specification")),
        "note": _section_md(ps.find("div", class_="note")),
        "samples": samples,
    }
