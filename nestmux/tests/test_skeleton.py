# -*- coding: utf-8 -*-

import pytest
from nestmux.skeleton import fib

__author__ = "Oivvio Polite"
__copyright__ = "Oivvio Polite"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
