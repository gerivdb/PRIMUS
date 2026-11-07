"""
Tests unitaires pour la primitive yaml_parser.
Critère : >= 5 tests (valid, invalid, empty, list root, nested).
"""
import pytest
from primitives.parsing.yaml_parser import yaml_parser


def test_yaml_parser_simple_key_value():
    """YAML simple clé:valeur retourne un dict."""
    result = yaml_parser("key: value\nname: PRIMUS\n")
    assert result == {"key": "value", "name": "PRIMUS"}


def test_yaml_parser_list_root():
    """YAML avec liste de premier niveau retourne une liste."""
    result = yaml_parser("- item1\n- item2\n- item3\n")
    assert result == ["item1", "item2", "item3"]


def test_yaml_parser_empty():
    """Chaîne vide retourne un dict vide."""
    assert yaml_parser("") == {}
    assert yaml_parser("   ") == {}


def test_yaml_parser_invalid_raises_valueerror():
    """YAML invalide lève une ValueError."""
    with pytest.raises(ValueError):
        yaml_parser(": : :\n{{{\n")


def test_yaml_parser_json_subset():
    """JSON valide (sous-ensemble YAML) est parsé."""
    result = yaml_parser('{"key": "value", "num": 42}')
    assert result == {"key": "value", "num": 42}


def test_yaml_parser_scalars():
    """Scalaires bool, null, int, float sont convertis."""
    result = yaml_parser("active: true\nempty: null\ncount: 10\nratio: 0.5\n")
    assert result == {"active": True, "empty": None, "count": 10, "ratio": 0.5}
