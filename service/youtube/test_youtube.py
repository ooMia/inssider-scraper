import unittest

from service.youtube.strategy import HashTagStrategy


class TestHashTagStrategy(unittest.TestCase):

    def test_parse_view_count(self):
        # 테스트 데이터를 (입력 문자열, 예상 출력) 형태의 튜플로 정의
        test_cases = [
            ("조회수 1.6억회", 160_000_000),
            ("조회수 1282만회", 12_820_000),
            ("조회수 1.8만회", 18_000),
            ("조회수 3.5천회", 3_500),
            ("조회수 329회", 329),
            ("조회수 없음", 0),
        ]

        # 각 테스트 케이스에 대해 검증
        for view_count_str, expected_count in test_cases:
            with self.subTest(view_count_str=view_count_str):
                self.assertEqual(
                    HashTagStrategy._parse_view_count(view_count_str), expected_count
                )


if __name__ == "__main__":
    unittest.main()
