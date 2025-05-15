import pytest

from model.repository import Post
from repository.handler import DatabaseManager


@pytest.fixture(scope="function", autouse=True)
def reset_db():
    DatabaseManager().drop_tables()
    DatabaseManager().create_tables()


def test_hierarchical_categories(sample_data):
    from repository.handler import DatabaseManager

    with DatabaseManager() as session:
        posts = session.query(Post).all()
        for post in posts:
            category = post.category
            root_category = category
            while root_category.upper_category is not None:
                root_category = root_category.upper_category

            assert f"[{root_category.name}({root_category.id})]" in post.title
            assert f"[{category.name}({category.id})]" in post.content


if __name__ == "__main__":
    import os

    import pytest

    pytest.main(["-s", os.path.abspath(__file__)])
