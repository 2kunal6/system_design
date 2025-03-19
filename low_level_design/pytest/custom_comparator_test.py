import pytest
import sys

sys.path.append('../')

from practice.custom_comparator import  Person

def test_cc():
    p1 = Person(1, 1)
    p2 = Person(2, 1)
    assert p1 == p2