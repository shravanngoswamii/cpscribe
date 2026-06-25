import os
from configparser import ConfigParser
from pathlib import Path

CONFIG_DIR = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "cpscribe"
CONFIG_FILE = CONFIG_DIR / "config"

DEFAULTS: dict[str, str] = {
    "blog_root": "",
    "author": "Shravan Goswami",
    "editor": "subl",
}


def load() -> dict[str, str]:
    cfg = dict(DEFAULTS)
    if CONFIG_FILE.exists():
        parser = ConfigParser()
        parser.read(CONFIG_FILE)
        if "cpscribe" in parser:
            cfg.update(parser["cpscribe"])
    if v := os.environ.get("CPSCRIBE_BLOG_ROOT"):
        cfg["blog_root"] = v
    if v := os.environ.get("CPSCRIBE_AUTHOR"):
        cfg["author"] = v
    return cfg


def save(cfg: dict[str, str]) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    parser = ConfigParser()
    parser["cpscribe"] = cfg
    with open(CONFIG_FILE, "w") as f:
        parser.write(f)


def init_interactive() -> None:
    cfg = load()
    print("cpscribe config\n")
    blog_root = input(f"Blog root [{cfg['blog_root'] or 'required'}]: ").strip()
    author = input(f"Author [{cfg['author']}]: ").strip()
    editor = input(f"Editor [{cfg['editor']}]: ").strip()
    cfg["blog_root"] = blog_root or cfg["blog_root"]
    cfg["author"] = author or cfg["author"]
    cfg["editor"] = editor or cfg["editor"]
    if not cfg["blog_root"]:
        raise SystemExit("blog_root is required")
    save(cfg)
    print(f"\nconfig saved to {CONFIG_FILE}")
