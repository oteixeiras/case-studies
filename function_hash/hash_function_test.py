import pytest

from main import hash_function

"""
    Run the tests with the command:
    1 - pip install pytest
    2 - pytest hash_function_test.py
"""


def test_hash_function_when_iguals_inputs():
    input_first = ["a", "b", "c"]
    input_second = ["a", "b", "c"]

    assert hash_function(input_first) == hash_function(input_second)


def test_hash_function_when_not_iguals_inputs():
    input_first = ["a", "b", "c"]
    input_second = ["A", "D", "c"]

    assert hash_function(input_first) != hash_function(input_second)


if __name__ == "__main__":
    pytest.main()
