import re


IP_PATTERN = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"


def find_logging_lines(config_text):
    # running-config에서 logging으로 시작하는 설정을 모두 찾는다.
    logging_lines = []

    for line in config_text.splitlines():
        stripped_line = line.strip()

        if stripped_line.startswith("logging "):
            logging_lines.append(stripped_line)

    return logging_lines


def has_ip_address(line):
    return re.search(IP_PATTERN, line) is not None


def check_n14_cisco(config_text):
    # N-14는 정책에 따른 로깅 설정 여부를 점검한다.
    # KISA 기준상 show logging 및 기관 로깅 정책 문서 확인이 필요하므로
    # running-config에서는 logging server 설정 존재 여부만 참고 증적으로 수집한다.
    found_settings = []
    weak_settings = []
    manual_settings = []

    logging_lines = find_logging_lines(config_text)

    for line in logging_lines:
        if has_ip_address(line):
            found_settings.append(f"logging server 설정 확인: {line}")

    if not found_settings:
        weak_settings.append("running-config 내 logging server 설정 없음")

    manual_settings.append("show logging 출력 정보 확인 필요")
    manual_settings.append("기관 로깅 정책 문서 확인 필요")
    manual_settings.append("정책에 따른 로그 레벨, 보관 대상, 보관 기간, 원격 전송 여부 확인 필요")
    manual_settings.append("보안사고 분석 및 법적 증적 확보 기준 충족 여부 확인 필요")

    result = "인터뷰 필요"

    return result, found_settings, weak_settings, manual_settings
