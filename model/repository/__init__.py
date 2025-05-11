"""
Conventions

1. 클래스명은 단수형의 카멜 케이스, 테이블은 복수형의 파스칼 케이스로 작성합니다.
    - 예시: 클래스 UserDetail, 테이블 user_details

2. relationship의 타입을 정의할 때 반드시 클래스명을 문자열로 작성합니다.
    - SQLAlchemy는 타입 힌트를 해석할 때, 해당 클래스가 정의된 시점에 이미 로드되어 있어야 합니다.
    서로 다른 도메인에 존재하는 테이블 간 양방향 참조 관계를 만들 때, 타입 정의 시 순환 참조가 발생합니다.
    이를 방지하기 위해서는 타입을 문자열로 작성해야 합니다.
    - 예시: user: Mapped["User"] = relationship(...)

3. 타입 힌트가 필요할 때는 TYPE_CHECKING을 사용합니다.
    - TYPE_CHECKING은 타입 힌트를 제공하기 위한 상수로, 실제 코드 실행 시에는 사용되지 않습니다.
    - 이 상수를 사용하면, 타입 힌트를 제공하면서도 순환 참조 문제를 피할 수 있습니다.
    - 예시:
        ```py
            from typing import TYPE_CHECKING
            if TYPE_CHECKING:
                from model.repository import Post
        ```
"""

# isort: skip_file
from .user import User  # noqa: F401
from .user import UserDetail, Follow  # noqa: F401
from .post import Post  # noqa: F401

from .video import Video  # noqa: F401
