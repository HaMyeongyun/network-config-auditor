import re


IP_PATTERN = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"


def is_logging_line(line):
    return line.startswith("logging ")


def has_ip_address(line):
    return re.search(IP_PATTERN, line) is not None


def find_logging_lines(config_text):
    # running-config에서 logging으로 시작하는 설정을 모두 찾는다.
    logging_lines = []

    for line in config_text.splitlines():
        stripped_line = line.strip()

        if is_logging_line(stripped_line):
            logging_lines.append(stripped_line)

    return logging_lines


def check_n11_cisco(config_text):
    # N-11은 원격 로그 서버 IP 설정 존재 여부를 기준으로 자동 판정한다.
    # trap, source-interface, facility 등 세부 로깅 정책은 수동확인 대상으로 분리한다.
    found_settings = []
    weak_settings = []
    manual_settings = []

    logging_lines = find_logging_lines(config_text)

    for line in logging_lines:
        if has_ip_address(line):
            found_settings.append(line)
        else:
            manual_settings.append(line)

    if not found_settings:
        weak_settings.append("원격 로그서버 IP 설정 없음")

    if weak_settings:
        result = "취약"
    else:
        result = "양호"

    return result, found_settings, weak_settings, manual_settings
