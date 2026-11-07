"""
Tests unitaires pour la primitive text_line_parser.
Critère : >= 4 tests (comments, empty lines, strip, unicode).
"""
import pytest
from primitives.parsing.text_line_parser import text_line_parser


def test_text_line_parser_basic():
    """Lignes normales sans commentaire sont retournées."""
    content = "alpha\nbeta\ngamma\n"
    assert text_line_parser(content) == ["alpha", "beta", "gamma"]


def test_text_line_parser_comments_filtered():
    """Lignes commençant par le caractère de commentaire sont filtrées."""
    content = "keep1\n# comment\nkeep2\n#autre comment\n"
    assert text_line_parser(content) == ["keep1", "keep2"]


def test_text_line_parser_empty_lines_filtered():
    """Lignes vides et espaces seuls sont filtrées."""
    content = "line1\n\n   \nline2\n"
    assert text_line_parser(content) == ["line1", "line2"]


def test_text_line_parser_custom_comment_char():
    """Caractère de commentaire personnalisé est respecté."""
    content = "data1\n// comment\ndata2\n"
    assert text_line_parser(content, comment_char="//") == ["data1", "data2"]


def test_text_line_parser_strip_false():
    """strip=False conserve les espaces autour des lignes."""
    content = "  spaced  \nplain\n"
    assert text_line_parser(content, strip=False) == ["  spaced  ", "plain"]


def test_text_line_parser_unicode():
    """Contenu Unicode est supporté."""
    content = "café\n# commentaire\nrésumé\n"
    assert text_line_parser(content) == ["café", "résumé"]
