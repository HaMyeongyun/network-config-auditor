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


def is_encrypted_password_line(line):
    # Packet Tracer/Cisco 4331 기준으로 secret 5는 MD5 해시 저장 방식이다.
    if line.startswith("enable secret 5") or " secret 5 " in line:
        return True

    # service password-encryption 적용 시 password 7 형태로 저장된다.
    if " password 7 " in line or line.startswith("password 7"):
        return True

    return False


def check_n03_cisco(config_text):
    # N-03은 Cisco running-config 기준으로 비밀번호 암호화 저장 여부를 점검한다.
    found_settings = []
    weak_settings = []

    password_lines = find_lines(
        config_text,
        [
            "enable secret",
            "enable password",
            "username",
            "password",
            "service password-encryption",
        ],
    )

    encryption_service_lines = find_lines(config_text, ["service password-encryption"])
    if encryption_service_lines:
        found_settings.extend(encryption_service_lines)

    for line in password_lines:
        if line.startswith("service password-encryption"):
            continue

        if is_encrypted_password_line(line):
            found_settings.append(line)
        else:
            weak_settings.append(f"평문 또는 암호화 미흡 비밀번호 설정: {line}")

    if not password_lines:
        weak_settings.append("비밀번호 관련 설정 없음")

    if weak_settings:
        result = "취약"
    else:
        result = "양호"

    return result, found_settings, weak_settings
