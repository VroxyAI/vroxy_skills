#!/usr/bin/env python3
"""Install the vroxy agent skills into every coding harness on the box.

  install_skills.py              copy the skills into each harness's skill root
  install_skills.py --dry-run    print what would change, change nothing
  install_skills.py --uninstall  remove the skills from every harness

A skill is a directory `<name>/SKILL.md`. Each harness reads skills from
its own root, so this walks the box, detects which harnesses are present
and copies the skills into each one — the same shape as the AWS CLI's
skill install, and the same harness detection as install-browser-mcp.

Stdlib only, on purpose: the install path is `curl | bash` onto a box
that may have nothing but python3.
"""
import argparse
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILLS_DIR = ROOT / "skills"

# harness binary (as resolved on PATH) -> skill root, relative to $HOME.
# Only the harnesses whose root is known-correct are listed; a new
# harness is one line here once its convention is confirmed.
HARNESS_ROOTS = {
    "claude":       ".claude/skills",
    "cursor-agent": ".cursor/skills",
    "codex":        ".codex/skills",
    "copilot":      ".copilot/skills",
    "opencode":     ".config/opencode/skills",
    "gemini":       ".agents/skills",
    "amp":          ".agents/skills",
}


def home() -> Path:
    return Path(os.environ.get("HOME", str(Path.home())))


def tool_env() -> dict:
    env = os.environ.copy()
    extra = [str(home() / ".local" / "bin"), str(home() / ".opencode" / "bin")]
    node_bins = sorted((home() / ".nvm" / "versions" / "node").glob("v*/bin"),
                       key=lambda p: tuple(int(x) for x in p.parent.name[1:].split(".") if x.isdigit()))
    if node_bins:
        extra.insert(0, str(node_bins[-1]))
    env["PATH"] = os.pathsep.join(extra + [env.get("PATH", "")])
    return env


def which(binary: str) -> str | None:
    return shutil.which(binary, path=tool_env()["PATH"])


def skill_names() -> list[str]:
    return sorted(p.name for p in SKILLS_DIR.iterdir() if (p / "SKILL.md").is_file())


def copy_skill(name: str, root: Path, dry_run: bool) -> str:
    src = SKILLS_DIR / name
    dst = root / name
    if (dst / "SKILL.md").is_file() and (dst / "SKILL.md").read_text() == (src / "SKILL.md").read_text():
        return "already installed"
    if dry_run:
        return f"would copy {src} -> {dst}"
    dst.mkdir(parents=True, exist_ok=True)
    for child in src.iterdir():
        if child.is_dir():
            shutil.copytree(child, dst / child.name, dirs_exist_ok=True)
        else:
            shutil.copy2(child, dst / child.name)
    return f"installed {dst}"


def remove_skill(name: str, root: Path, dry_run: bool) -> str:
    dst = root / name
    if not dst.exists():
        return "not present"
    if dry_run:
        return f"would remove {dst}"
    shutil.rmtree(dst)
    return f"removed {dst}"


def install(dry_run: bool) -> list[tuple[str, bool, str]]:
    names = skill_names()
    results: list[tuple[str, bool, str]] = []
    for harness, root_rel in HARNESS_ROOTS.items():
        if not which(harness):
            continue
        root = home() / root_rel
        for name in names:
            try:
                results.append((harness, True, copy_skill(name, root, dry_run)))
            except OSError as exc:
                results.append((harness, False, f"{root / name}: {exc}"))
    return results


def uninstall(dry_run: bool) -> list[tuple[str, bool, str]]:
    names = skill_names()
    results: list[tuple[str, bool, str]] = []
    for harness, root_rel in HARNESS_ROOTS.items():
        root = home() / root_rel
        for name in names:
            try:
                results.append((harness, True, remove_skill(name, root, dry_run)))
            except OSError as exc:
                results.append((harness, False, f"{root / name}: {exc}"))
    return results


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="install_skills", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="change nothing")
    parser.add_argument("--uninstall", action="store_true", help="remove the skills instead")
    args = parser.parse_args(argv)

    results = uninstall(args.dry_run) if args.uninstall else install(args.dry_run)
    if not results:
        print("no known harnesses found on PATH")
    for harness, ok, detail in results:
        print(f"{'✓' if ok else '✗'} {harness:13} {detail}")
    return 0 if all(ok for _, ok, _ in results) else 1


if __name__ == "__main__":
    sys.exit(main())
