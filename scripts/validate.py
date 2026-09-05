#!/usr/bin/env python3
"""Check this repository's dual-plugin packaging conventions, without installing it."""
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def frontmatter(path):
    parts = path.read_text(encoding="utf-8").split("---", 2)
    require(len(parts) == 3 and not parts[0].strip(), f"{path}: missing frontmatter")
    data = yaml.safe_load(parts[1])
    require(isinstance(data, dict) and parts[2].strip(), f"{path}: empty metadata/body")
    require(isinstance(data.get("description"), str) and data["description"].strip(), f"{path}: missing description")
    return data


def main():
    claude = read_json(ROOT / ".claude-plugin/marketplace.json")
    codex = read_json(ROOT / ".agents/plugins/marketplace.json")
    require(claude["name"] == codex["name"], "Marketplace names differ")
    catalogs = []
    for catalog, platform in ((claude, "claude"), (codex, "codex")):
        entries = {}
        for entry in catalog["plugins"]:
            name = entry["name"]
            require(name not in entries, f"Duplicate plugin: {name}")
            source = entry["source"]
            if platform == "codex":
                require(source["source"] == "local", "Expected local Codex plugin source")
                require(entry["policy"]["installation"] in {"AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"}, "Invalid installation policy")
                require(entry["policy"]["authentication"] in {"ON_INSTALL", "ON_USE"}, "Invalid authentication policy")
                require(bool(entry["category"]), "Missing category")
                source = source["path"]
            require(source == f"./plugins/{name}", f"Invalid source: {source}")
            entries[name] = source
        catalogs.append(entries)
    require(catalogs[0] == catalogs[1] and catalogs[0], "Catalogs differ or are empty")
    folders = {p.name for p in (ROOT / "plugins").iterdir() if p.is_dir()}
    require(folders == set(catalogs[0]), "Unregistered or missing plugin folder")
    for name in catalogs[0]:
        root = ROOT / "plugins" / name
        manifests = [read_json(root / f".{platform}-plugin/plugin.json") for platform in ("claude", "codex")]
        require(all(m["name"] == name for m in manifests), f"{name}: name mismatch")
        require(manifests[0]["version"] == manifests[1]["version"], f"{name}: version mismatch")
        require(re.fullmatch(r"\d+\.\d+\.\d+", manifests[0]["version"]), f"{name}: use stable x.y.z versions")
        require(manifests[1]["skills"] == "./skills/", f"{name}: invalid skills path")
        skills = list((root / "skills").iterdir())
        require(bool(skills), f"{name}: no skills")
        skill_names = set()
        for skill in skills:
            require(skill.is_dir(), f"{skill}: expected skill directory")
            data = frontmatter(skill / "SKILL.md")
            require(data.get("name") == skill.name, f"{skill}: name mismatch")
            require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill.name) and len(skill.name) <= 64, f"{skill}: invalid name")
            skill_names.add(skill.name)
        for command in (root / "commands").glob("*.md"):
            frontmatter(command)
            require(command.stem not in skill_names, f"{command}: command/skill collision")
        for agent in (root / "agents").glob("*.md"):
            require(frontmatter(agent).get("name") == agent.stem, f"{agent}: name mismatch")
        for path in root.rglob("*"):
            require(not path.is_symlink(), f"{path}: use archive-local files, not symlinks")
        print(f"PASS {name}: both manifests, catalogs, skills, commands, agents")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, yaml.YAMLError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
