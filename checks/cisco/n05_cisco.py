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


def check_required_privilege_commands(config_text):
    # N-05 가이드에서 level 15 적용이 필요하다고 보는 중요 명령어 목록이다.
    required_commands = [
        "connect",
        "telnet",
        "rlogin",
        "show ip access-list",
        "show logging",
    ]

    found_settings = []
    weak_settings = []

    for command in required_commands:
        expected_line = f"privilege exec level 15 {command}"

        if expected_line in config_text:
            found_settings.append(expected_line)
        else:
            weak_settings.append(f"{command} 명령어 level 15 미설정")

    return found_settings, weak_settings


def check_n05_cisco(config_text):
    # N-05는 중요 명령어 level 15 설정을 자동 점검한다.
    # username 계정별 권한은 운영 목적 확인이 필요하므로 항상 수동확인 대상으로 출력한다.
    found_settings = []
    weak_settings = []
    manual_settings = []

    command_found, command_weak = check_required_privilege_commands(config_text)
    username_lines = find_lines(config_text, ["username"])

    found_settings.extend(command_found)
    weak_settings.extend(command_weak)
    manual_settings.extend(username_lines)

    if weak_settings:
        result = "취약"
    elif manual_settings:
        result = "수동확인"
    else:
        result = "양호"

    return result, found_settings, weak_settings, manual_settings
