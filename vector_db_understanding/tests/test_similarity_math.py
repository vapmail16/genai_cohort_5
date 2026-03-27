"""Tests for similarity_math (TDD)."""

import math

import pytest

from similarity_math import (
    cosine_similarity,
    dot_product,
    euclidean_distance,
    manhattan_distance,
)


def test_dot_product_worked_example():
    assert dot_product([2, 3], [4, 1]) == 11


def test_dot_product_length_mismatch():
    with pytest.raises(ValueError):
        dot_product([1], [1, 2])


def test_cosine_worked_example():
    a = [1.0, 0.0]
    b = [1.0, 1.0]
    assert abs(cosine_similarity(a, b) - 1 / math.sqrt(2)) < 1e-9


def test_cosine_zero_norm_returns_zero():
    assert cosine_similarity([0, 0], [1, 1]) == 0.0


def test_euclidean_3_4_5():
    assert abs(euclidean_distance([0, 0], [3, 4]) - 5.0) < 1e-9


def test_manhattan_worked_example():
    assert manhattan_distance([1, 2], [4, 6]) == 7
