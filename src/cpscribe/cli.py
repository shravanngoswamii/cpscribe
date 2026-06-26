import argparse
import subprocess
import sys
from pathlib import Path

from cpscribe import __version__, generator, scraper
from cpscribe import config as cfg


def cmd_init(_args) -> None:
    cfg.init_interactive()


def cmd_post(args) -> None:
    conf = cfg.load()
    if not conf["blog_root"]:
        sys.exit("blog_root not configured -- run `cpscribe init` first")

    if args.input.endswith(".cpp"):
        cpp_file = Path(args.input)
        if not cpp_file.exists():
            sys.exit(f"file not found: {cpp_file}")
        url = scraper.extract_url_from_cpp(cpp_file.read_text())
        if not url:
            sys.exit(f"no Codeforces URL found in {cpp_file}")
    else:
        url = args.input
        cpp_file = Path(args.solution) if args.solution else None

    contest_id, index = scraper.parse_url(url)

    if cpp_file is None:
        cpp_file = Path(f"{index}.cpp")
    cpp_code = cpp_file.read_text().strip() if cpp_file.exists() else "// paste your solution here"

    print(f"fetching CF{contest_id}{index}...")
    problem = scraper.scrape(contest_id, index, url)
    print(f"  {index}. {problem['name']}  {problem['rating']}  {problem['contest']}")
    print(f"  {len(problem['samples'])} sample(s)  {problem['time_lim']}  {problem['mem_lim']}")

    out_dir = Path(conf["blog_root"]) / contest_id
    out_file = out_dir / f"{index}.md"
    out_dir.mkdir(parents=True, exist_ok=True)

    if out_file.exists() and not args.force:
        sys.exit(f"already exists: {out_file}  (--force to overwrite)")

    out_file.write_text(generator.build(contest_id, index, problem, cpp_code, conf["author"]))
    print(f"created: {out_file}")

    editor = args.editor or conf["editor"]
    if editor:
        subprocess.Popen([editor, str(out_file)])


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="cpscribe",
        description="Generate blog posts for competitive programming solutions",
    )
    parser.add_argument("-v", "--version", action="version", version=f"cpscribe {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Configure cpscribe interactively")

    post = sub.add_parser("post", help="Generate a blog post for a Codeforces problem")
    post.add_argument("input", metavar="URL|file.cpp")
    post.add_argument("solution", nargs="?", metavar="solution.cpp")
    post.add_argument("--force", action="store_true", help="overwrite existing post")
    post.add_argument("--editor", metavar="CMD")

    args = parser.parse_args()
    {"init": cmd_init, "post": cmd_post}[args.command](args)
