#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from primitives.parsing.repo_tree_parser import repo_tree_parser, flatten_tree, find_in_tree


def test_parse_string_paths():
    entries = ["src/foo/bar.py", "src/foo/baz.py", "README.md"]
    root = repo_tree_parser(entries)
    flat = flatten_tree(root)
    assert "src/foo/bar.py" in flat
    assert "README.md" in flat


def test_parse_github_api_dicts():
    entries = [
        {"path": "primitives/parsing/repo_tree_parser.py", "type": "file"},
        {"path": "primitives/parsing", "type": "dir"},
        {"path": "README.md", "type": "file"},
    ]
    root = repo_tree_parser(entries)
    assert any(c["name"] == "primitives" for c in root["children"])


def test_nested_structure():
    entries = ["a/b/c/d.py", "a/b/e.py", "a/f.py"]
    root = repo_tree_parser(entries)
    a_node = next(c for c in root["children"] if c["name"] == "a")
    assert a_node["type"] == "dir"
    b_node = next(c for c in a_node["children"] if c["name"] == "b")
    assert any(c["name"] == "c" for c in b_node["children"])


def test_empty_input():
    root = repo_tree_parser([])
    assert root["children"] == []


def test_find_in_tree():
    entries = ["src/utils/parser.py", "tests/test_parser.py"]
    root = repo_tree_parser(entries)
    results = find_in_tree(root, "parser.py")
    assert len(results) == 1
    assert results[0]["name"] == "parser.py"


def test_flatten_roundtrip():
    entries = ["a/b.py", "c/d/e.py", "f.py"]
    root = repo_tree_parser(entries)
    flat = flatten_tree(root)
    for p in entries:
        assert p in flat


if __name__ == "__main__":
    test_parse_string_paths()
    test_parse_github_api_dicts()
    test_nested_structure()
    test_empty_input()
    test_find_in_tree()
    test_flatten_roundtrip()
    print("✅ All repo_tree_parser tests passed")
