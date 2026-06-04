def find_lines(config_text, keywords):
    # 전체 설정에서 특정 키워드로 시작하는 줄을 찾는다.
    matched_lines = []

    for line in config_text.splitlines():
        stripped_line = line.strip()

        for keyword in keywords:
            if stripped_line.startswith(keyword):
                matched_lines.append(stripped_line)
                break
    return matched_lines


def get_min_length_value(line):
    # 예: "security passwords min-length 8"에서 마지막 값인 8을 숫자로 꺼낸다.
    parts = line.split()

    if not parts:
        return None

    try:
        return int(parts[-1])
    except ValueError:
        return None


def check_n02_cisco(config_text):
    # N-02는 Cisco 기준으로 비밀번호 최소 길이 정책이 8 이상인지 점검한다.
    found_settings = []
    weak_settings = []

    min_length_lines = find_lines(config_text, ["security passwords min-length"])

    if not min_length_lines:
        weak_settings.append("비밀번호 최소 길이 정책 미설정")
    else:
        for line in min_length_lines:
            min_length = get_min_length_value(line)

            if min_length is None:
                weak_settings.append(f"비밀번호 최소 길이 값 확인 불가: {line}")
            elif min_length >= 8:
                found_settings.append(line)
            else:
                weak_settings.append(f"비밀번호 최소 길이 기준 미달: {line}")

    if weak_settings:
        result = "취약"
    else:
        result = "양호"

    return result, found_settings, weak_settings
