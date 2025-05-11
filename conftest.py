import pytest


def pytest_addoption(parser):
    parser.addoption("--test-slow", action="store_true", help="run slow tests")


def pytest_runtest_setup(item):
    if "slow" in item.keywords and not item.config.getoption("--test-slow"):
        pytest.skip("use --test-slow to run this test")
