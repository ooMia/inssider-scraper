from sqlalchemy.orm import Session

from model.repository import Category, Post, User, UserDetail


# 내부용 인스턴스 생성 함수 (언더바로 시작)
def _intern_create_users(session: Session):
    user1 = User(email="hong@test.com", password="pw1", password_salt="salt1")
    user2 = User(email="kim@test.com", password="pw2", password_salt="salt2")
    user3 = User(email="lee@test.com", password="pw3", password_salt="salt3")
    session.add_all([user1, user2, user3])
    session.commit()

    user_detail1 = UserDetail(user=user1, username="홍길동")
    user_detail2 = UserDetail(user=user2, username="김철수")
    user_detail3 = UserDetail(user=user3, username="이영희")
    session.add_all([user_detail1, user_detail2, user_detail3])
    session.commit()
    return {
        "users": [user1, user2, user3],
        "user_details": [user_detail1, user_detail2, user_detail3],
    }


def _intern_create_categories(session: Session):
    level1 = Category(name="계층1", upper_category_id=None)
    level1_1 = Category(name="계층1-1", upper_category=level1)
    level1_1_a = Category(name="계층1-1-A", upper_category=level1_1)
    level1_1_b = Category(name="계층1-1-B", upper_category=level1_1)
    level1_2 = Category(name="계층1-2", upper_category=level1)
    level2 = Category(name="계층2", upper_category_id=None)
    level2_1 = Category(name="계층2-1", upper_category=level2)
    categories = [level1, level1_1, level1_1_a, level1_1_b, level1_2, level2, level2_1]
    session.add_all(categories)
    session.commit()
    return categories


def _intern_create_posts(session: Session, users, categories):

    def _get_root_category(category):
        current = category
        while current.upper_category is not None:
            current = current.upper_category
        return current

    posts = []
    for idx, category in enumerate(categories):
        root_category = _get_root_category(category)
        post = Post(
            title=f"[{root_category.name}({root_category.id})] 카테고리 관련 글",
            content=f"이 글은 [{category.name}({category.id})] 카테고리에 속합니다.",
            media_url="https://picsum.photos/200",
            user=users[idx % len(users)],
            category=category,
        )
        session.add(post)
        posts.append(post)
    session.commit()
    return posts


# 공개 인터페이스: 서비스 전체 샘플 데이터 생성
def create_sample_data(session: Session):
    """
    서비스가 일정 기간 운영된 상태를 재현하는 샘플 데이터 전체를 생성합니다.
    """
    user_data = _intern_create_users(session)
    categories = _intern_create_categories(session)
    posts = _intern_create_posts(session, user_data["users"], categories)
    return {
        "users": user_data["users"],
        "user_details": user_data["user_details"],
        "categories": categories,
        "posts": posts,
    }
