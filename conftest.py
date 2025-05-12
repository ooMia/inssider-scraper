import pytest


def pytest_addoption(parser):
    parser.addoption("--test-slow", action="store_true", help="run slow tests")


def pytest_runtest_setup(item):
    if "slow" in item.keywords and not item.config.getoption("--test-slow"):
        pytest.skip("use --test-slow to run this test")


@pytest.fixture
def sample_data():
    """
    통합 샘플 데이터를 DB에 생성하고, 딕셔너리 형태로 반환합니다.
    """
    from model.repository.test import create_sample_data
    from repository.handler import DatabaseManager

    with DatabaseManager() as session:
        data = create_sample_data(session)
        yield data
        # 필요하다면 정리(cleanup) 코드 추가
