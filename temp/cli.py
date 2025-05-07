import argparse
import hashlib
import os
from urllib.parse import urlparse

from scrape.youtube import DefaultCrawler, YouTube


def __url_to_filename(url):
    """URL을 파일 이름으로 변환"""
    # TODO move to utils
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    key = hashlib.md5(url.encode("utf-8")).hexdigest()
    return f"{domain}/{key}.html"


def __write_to_file(file_path, content):
    """파일에 내용을 씁니다. 디렉토리가 없으면 생성합니다."""
    # TODO move to utils
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)
    with open(file_path, "w+", encoding="utf-8") as f:
        f.write(content)


def main():
    """웹 스크래핑을 위한 CLI 진입점"""
    parser = argparse.ArgumentParser(description="SNS Web Scraper")
    parser.add_argument("--url", help="스크래핑 할 URL")
    parser.add_argument("--base", help="결과 저장 기준 경로")

    args = parser.parse_args()

    if args.url:
        print(f"스크래핑 시작: {args.url}")
        file_name = __url_to_filename(args.url)
        base = args.base if args.base else os.path.join(os.getcwd(), "data")
        output_path = f"{base}/{file_name}"

        if not os.path.exists(output_path):
            data = DefaultCrawler().scrape(args.url)
            __write_to_file(output_path, data)
        print(f"URL이 {output_path}에 저장되었습니다.")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
