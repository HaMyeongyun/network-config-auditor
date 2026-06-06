def find_timestamp_lines(config_text):
    # Cisco 로그 timestamp 관련 설정을 찾는다.
    timestamp_lines = []
    disabled_lines = []

    for line in config_text.splitlines():
        stripped_line = line.strip()

        if stripped_line.startswith("service timestamps log"):
            timestamp_lines.append(stripped_line)
        elif stripped_line.startswith("no service timestamps log"):
            disabled_lines.append(stripped_line)

    return timestamp_lines, disabled_lines


def check_n16_cisco(config_text):
    # N-16은 Cisco 기준으로 로그 timestamp 설정 여부를 점검한다.
    found_settings = []
    weak_settings = []

    timestamp_lines, disabled_lines = find_timestamp_lines(config_text)

    if timestamp_lines:
        found_settings.extend(timestamp_lines)
    elif disabled_lines:
        weak_settings.extend(disabled_lines)
    else:
        weak_settings.append("service timestamps log 설정 없음")

    if weak_settings:
        result = "취약"
    else:
        result = "양호"

    return result, found_settings, weak_settings
