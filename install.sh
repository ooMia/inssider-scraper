#!/bin/bash

# name: install.sh
# description: project setup script
# prerequisites: python3, pip3, jq

# 함수 정의
function print_usage() {
    echo "사용법: $0 [옵션]"
    echo "옵션:"
    echo "  -h, --help    도움말 출력"
    echo "  -v, --version 버전 정보 출력"
}

function print_version() {
   jq -r '.version' package.json
}

function main() {
    echo "install start"
    pip install --upgrade pip -q
    pip install -U python-dotenv -q
    pip install -U PyYAML -q
    pip install -U pytest -q
    pip install -U pytest-cov -q
    pip install selenium -q
    pip install beautifulsoup4 -q
    pip install pyautogui -q
    pip freeze --require-virtualenv > requirements.txt
    echo "installed successfully"
}

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -h|--help) print_usage; exit 0 ;;
        -v|--version) print_version; exit 0 ;;
        *) echo "알 수 없는 옵션: $1"; print_usage; exit 1 ;;
    esac
done

set -e
main
