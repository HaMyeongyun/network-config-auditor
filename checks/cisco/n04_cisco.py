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


def get_attempts_value(line):
    # 예: "login block-for 120 attempts 3 within 60"에서 attempts 뒤의 값인 3을 꺼낸다.
    parts = line.split()

    if "attempts" not in parts:
        return None

    attempts_index = parts.index("attempts")
    value_index = attempts_index + 1

    if value_index >= len(parts):
        return None

    try:
        return int(parts[value_index])
    except ValueError:
        return None


def check_n04_cisco(config_text):
    # N-04는 Cisco 기준으로 로그인 실패 임계값이 5회 이하인지 점검한다.
    found_settings = []
    weak_settings = []

    block_for_lines = find_lines(config_text, ["login block-for"])

    if not block_for_lines:
        weak_settings.append("로그인 실패 잠금 임계값 미설정")
    else:
        for line in block_for_lines:
            attempts = get_attempts_value(line)

            if attempts is None:
                weak_settings.append(f"로그인 실패 임계값 확인 불가: {line}")
            elif attempts <= 5:
                found_settings.append(line)
            else:
                weak_settings.append(f"로그인 실패 임계값 기준 초과: {line}")

    if weak_settings:
        result = "취약"
    else:
        result = "양호"

    return result, found_settings, weak_settings
