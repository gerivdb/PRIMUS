# Tests PRIMUS Registry — Registre et Loader des primitives
# IntentHash: 0xTEST_PRIMUS_REGISTRY_20260808

import json
import os
import tempfile
from pathlib import Path

import pytest

from src.primus.registry import (
    PrimitiveDefinition,
    PrimitiveRegistry,
    PrimitiveType,
    Priority,
    RegistryStats,
    create_registry_from_paths,
)
from src.primus.loader import (
    PrimitiveLoadError,
    PrimitiveValidationError,
    load_primitive_directory,
    load_primitive_file,
)


# ============================================================
# Helpers
# ============================================================

def _make_primitive_data(overrides: dict = None) -> dict:
    """Crée un dict de primitive valide pour les tests."""
    data = {
        "name": "test-primitive",
        "version": "1.0.0",
        "type": "parser",
        "strate": "L4",
        "priority": "P1",
        "input": {"data": {"type": "object"}},
        "output": {"result": {"type": "object"}},
        "tools": ["tool-a"],
        "description": "Test primitive",
        "intent_hash": "0xTEST_20260808",
    }
    if overrides:
        data.update(overrides)
    return data


def _write_yaml(path: Path, data: dict) -> None:
    """Écrit un dict en YAML minimal (sans PyYAML)."""
    lines = []
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{key}:")
            for k, v in value.items():
                lines.append(f"  {k}: {v}")
        elif isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {item}")
        elif isinstance(value, bool):
            lines.append(f"{key}: {str(value).lower()}")
        else:
            lines.append(f"{key}: {value}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_json(path: Path, data: dict) -> None:
    """Écrit un dict en JSON."""
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


# ============================================================
# Tests PrimitiveDefinition
# ============================================================

class TestPrimitiveDefinition:
    """Tests pour PrimitiveDefinition."""

    def test_creation_valid(self):
        p = PrimitiveDefinition(
            name="test",
            version="1.0.0",
            type=PrimitiveType.PARSER,
            strate="L4",
            priority=Priority.P1,
        )
        assert p.name == "test"
        assert p.version == "1.0.0"
        assert p.type == PrimitiveType.PARSER
        assert p.strate == "L4"
        assert p.priority == Priority.P1

    def test_creation_with_all_fields(self):
        p = PrimitiveDefinition(
            name="full",
            version="2.0.0",
            type=PrimitiveType.EXECUTOR,
            strate="L3",
            priority=Priority.P2,
            input={"x": {"type": "int"}},
            output={"y": {"type": "int"}},
            tools=["tool1", "tool2"],
            description="Full primitive",
            intent_hash="0xABC",
        )
        assert p.input == {"x": {"type": "int"}}
        assert p.output == {"y": {"type": "int"}}
        assert p.tools == ["tool1", "tool2"]
        assert p.description == "Full primitive"
        assert p.intent_hash == "0xABC"

    def test_empty_name_raises(self):
        with pytest.raises(ValueError, match="name"):
            PrimitiveDefinition(
                name="",
                version="1.0.0",
                type=PrimitiveType.PARSER,
                strate="L4",
                priority=Priority.P1,
            )

    def test_empty_version_raises(self):
        with pytest.raises(ValueError, match="version"):
            PrimitiveDefinition(
                name="test",
                version="",
                type=PrimitiveType.PARSER,
                strate="L4",
                priority=Priority.P1,
            )

    def test_frozen_immutable(self):
        p = PrimitiveDefinition(
            name="test",
            version="1.0.0",
            type=PrimitiveType.PARSER,
            strate="L4",
            priority=Priority.P1,
        )
        with pytest.raises(AttributeError):
            p.name = "changed"  # type: ignore


# ============================================================
# Tests PrimitiveRegistry
# ============================================================

class TestPrimitiveRegistry:
    """Tests pour PrimitiveRegistry."""

    def test_empty_registry(self):
        registry = PrimitiveRegistry()
        assert len(registry) == 0
        assert registry.list_all() == []

    def test_register_single(self):
        registry = PrimitiveRegistry()
        p = PrimitiveDefinition(
            name="p1",
            version="1.0.0",
            type=PrimitiveType.PARSER,
            strate="L4",
            priority=Priority.P1,
        )
        registry._register(p)
        assert len(registry) == 1
        assert registry.has("p1")
        assert "p1" in registry

    def test_register_duplicate_raises(self):
        registry = PrimitiveRegistry()
        p1 = PrimitiveDefinition(
            name="dup", version="1.0.0", type=PrimitiveType.PARSER,
            strate="L4", priority=Priority.P1,
        )
        p2 = PrimitiveDefinition(
            name="dup", version="2.0.0", type=PrimitiveType.PARSER,
            strate="L4", priority=Priority.P1,
        )
        registry._register(p1)
        with pytest.raises(ValueError, match="Duplicate"):
            registry._register(p2)

    def test_get_existing(self):
        registry = PrimitiveRegistry()
        p = PrimitiveDefinition(
            name="p1", version="1.0.0", type=PrimitiveType.PARSER,
            strate="L4", priority=Priority.P1,
        )
        registry._register(p)
        assert registry.get("p1") == p

    def test_get_missing_raises(self):
        registry = PrimitiveRegistry()
        with pytest.raises(KeyError, match="not found"):
            registry.get("missing")

    def test_list_by_type(self):
        registry = PrimitiveRegistry()
        p1 = PrimitiveDefinition(
            name="p1", version="1.0.0", type=PrimitiveType.PARSER,
            strate="L4", priority=Priority.P1,
        )
        p2 = PrimitiveDefinition(
            name="p2", version="1.0.0", type=PrimitiveType.EXECUTOR,
            strate="L4", priority=Priority.P1,
        )
        registry._register(p1)
        registry._register(p2)
        
        parsers = registry.list_by_type(PrimitiveType.PARSER)
        assert len(parsers) == 1
        assert parsers[0].name == "p1"

    def test_list_by_strate(self):
        registry = PrimitiveRegistry()
        p1 = PrimitiveDefinition(
            name="p1", version="1.0.0", type=PrimitiveType.PARSER,
            strate="L4", priority=Priority.P1,
        )
        p2 = PrimitiveDefinition(
            name="p2", version="1.0.0", type=PrimitiveType.PARSER,
            strate="L3", priority=Priority.P1,
        )
        registry._register(p1)
        registry._register(p2)
        
        l4_prims = registry.list_by_strate("L4")
        assert len(l4_prims) == 1
        assert l4_prims[0].name == "p1"

    def test_list_by_priority(self):
        registry = PrimitiveRegistry()
        p1 = PrimitiveDefinition(
            name="p1", version="1.0.0", type=PrimitiveType.PARSER,
            strate="L4", priority=Priority.P1,
        )
        p2 = PrimitiveDefinition(
            name="p2", version="1.0.0", type=PrimitiveType.PARSER,
            strate="L4", priority=Priority.P2,
        )
        registry._register(p1)
        registry._register(p2)
        
        p1_prims = registry.list_by_priority(Priority.P1)
        assert len(p1_prims) == 1
        assert p1_prims[0].name == "p1"

    def test_stats(self):
        registry = PrimitiveRegistry()
        p1 = PrimitiveDefinition(
            name="p1", version="1.0.0", type=PrimitiveType.PARSER,
            strate="L4", priority=Priority.P1,
        )
        p2 = PrimitiveDefinition(
            name="p2", version="1.0.0", type=PrimitiveType.EXECUTOR,
            strate="L3", priority=Priority.P2,
        )
        registry._register(p1)
        registry._register(p2)
        
        stats = registry.stats()
        assert stats.total == 2
        assert stats.by_type["parser"] == 1
        assert stats.by_type["executor"] == 1
        assert stats.by_strate["L4"] == 1
        assert stats.by_strate["L3"] == 1
        assert stats.by_priority["P1"] == 1
        assert stats.by_priority["P2"] == 1


# ============================================================
# Tests load_primitive_file (YAML)
# ============================================================

class TestLoadPrimitiveFile:
    """Tests pour load_primitive_file avec YAML."""

    def test_load_valid_yaml(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as f:
            _write_yaml(Path(f.name), _make_primitive_data())
            f.flush()
            
            p = load_primitive_file(f.name)
            assert p.name == "test-primitive"
            assert p.version == "1.0.0"
            assert p.type == PrimitiveType.PARSER
            assert p.strate == "L4"
            assert p.priority == Priority.P1
        
        os.unlink(f.name)

    def test_load_valid_json(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            data = _make_primitive_data()
            json.dump(data, f)
            f.flush()
            
            p = load_primitive_file(f.name)
            assert p.name == "test-primitive"
            assert p.type == PrimitiveType.PARSER
        
        os.unlink(f.name)

    def test_load_missing_file_raises(self):
        with pytest.raises(FileNotFoundError):
            load_primitive_file("/nonexistent/path/primitive.yaml")

    def test_load_unsupported_extension_raises(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write("name: test\n")
            f.flush()
            
            with pytest.raises(PrimitiveLoadError, match="Unsupported"):
                load_primitive_file(f.name)
        
        os.unlink(f.name)

    def test_load_missing_name_raises(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as f:
            data = _make_primitive_data()
            del data["name"]
            _write_yaml(Path(f.name), data)
            f.flush()
            
            with pytest.raises(PrimitiveValidationError, match="name"):
                load_primitive_file(f.name)
        
        os.unlink(f.name)

    def test_load_invalid_type_raises(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as f:
            data = _make_primitive_data({"type": "invalid_type"})
            _write_yaml(Path(f.name), data)
            f.flush()
            
            with pytest.raises(PrimitiveValidationError, match="type"):
                load_primitive_file(f.name)
        
        os.unlink(f.name)

    def test_load_invalid_priority_raises(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as f:
            data = _make_primitive_data({"priority": "P99"})
            _write_yaml(Path(f.name), data)
            f.flush()
            
            with pytest.raises(PrimitiveValidationError, match="priority"):
                load_primitive_file(f.name)
        
        os.unlink(f.name)


# ============================================================
# Tests load_primitive_directory
# ============================================================

class TestLoadPrimitiveDirectory:
    """Tests pour load_primitive_directory."""

    def test_load_directory_empty(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            results = load_primitive_directory(tmpdir, lambda p: None)
            assert results == []

    def test_load_directory_multiple(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            
            # Créer 2 primitives YAML
            data1 = _make_primitive_data({"name": "prim-a", "type": "parser"})
            data2 = _make_primitive_data({"name": "prim-b", "type": "validator"})
            _write_yaml(tmp / "prim-a.yaml", data1)
            _write_yaml(tmp / "prim-b.yaml", data2)
            
            registry = PrimitiveRegistry()
            results = load_primitive_directory(tmpdir, registry._register)
            
            assert len(results) == 2
            assert "prim-a" in results
            assert "prim-b" in results
            assert len(registry) == 2

    def test_load_directory_skips_invalid(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            
            # Fichier valide
            data1 = _make_primitive_data({"name": "valid"})
            _write_yaml(tmp / "valid.yaml", data1)
            
            # Fichier invalide (pas de name)
            data2 = _make_primitive_data()
            del data2["name"]
            _write_yaml(tmp / "invalid.yaml", data2)
            
            # Fichier non-YAML
            (tmp / "readme.txt").write_text("hello", encoding="utf-8")
            
            registry = PrimitiveRegistry()
            results = load_primitive_directory(tmpdir, registry._register)
            
            assert len(results) == 1
            assert "valid" in results


# ============================================================
# Tests create_registry_from_paths
# ============================================================

class TestCreateRegistryFromPaths:
    """Tests pour create_registry_from_paths."""

    def test_from_file(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as f:
            _write_yaml(Path(f.name), _make_primitive_data({"name": "from-file"}))
            f.flush()
            
            registry = create_registry_from_paths([f.name])
            assert len(registry) == 1
            assert registry.has("from-file")
        
        os.unlink(f.name)

    def test_from_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            data = _make_primitive_data({"name": "from-dir"})
            _write_yaml(tmp / "p.yaml", data)
            
            registry = create_registry_from_paths([tmpdir])
            assert len(registry) == 1
            assert registry.has("from-dir")

    def test_from_mixed_paths(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            data1 = _make_primitive_data({"name": "file-only"})
            data2 = _make_primitive_data({"name": "dir-only"})
            _write_yaml(tmp / "p.yaml", data1)
            _write_yaml(tmp / "p2.yaml", data2)
            
            # Load directory only (contains p.yaml and p2.yaml)
            registry = create_registry_from_paths([tmp])
            assert len(registry) == 2
            assert registry.has("file-only")
            assert registry.has("dir-only")


# ============================================================
# Tests REGISTRY.yaml (fichier réel)
# ============================================================

class TestRealRegistryYaml:
    """Tests sur le vrai fichier REGISTRY.yaml du repo."""

    def test_load_real_registry(self):
        registry = PrimitiveRegistry()
        registry.load_file("REGISTRY.yaml")
        assert len(registry) >= 1

    def test_real_registry_has_registry_loader(self):
        registry = PrimitiveRegistry()
        registry.load_file("REGISTRY.yaml")
        assert registry.has("registry-loader")
        
        p = registry.get("registry-loader")
        assert p.type == PrimitiveType.EXECUTOR
        assert p.strate == "L4"
        assert p.priority == Priority.P1
        assert "registry_path" in p.input
        assert "loaded_count" in p.output

    def test_real_registry_stats(self):
        registry = PrimitiveRegistry()
        registry.load_file("REGISTRY.yaml")
        stats = registry.stats()
        assert stats.total >= 1
        assert "executor" in stats.by_type


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
