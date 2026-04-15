import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import recommend, search_products


def test_recommend_found():
    result = recommend("Smart")
    assert isinstance(result, list)
    assert len(result) > 0


def test_recommend_not_found():
    result = recommend("xyzabc999")
    assert result == []


def test_recommend_case_insensitive():
    result1 = recommend("smart")
    result2 = recommend("SMART")
    assert result1 == result2


def test_recommend_cached():
    result1 = recommend("Gaming")
    result2 = recommend("Gaming")
    assert result1 == result2


def test_search_found():
    result = search_products("hoodie")
    assert len(result) >= 1


def test_search_not_found():
    result = search_products("xyzabc999")
    assert result == []
