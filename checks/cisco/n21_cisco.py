def find_tftp_settings(config_text):
    # Cisco에서 TFTP 서버 기능 또는 자동 설정 로드 관련 설정을 찾는다.
    tftp_settings = []
    manual_settings = []

    for line in config_text.splitlines():
        stripped_line = line.strip()

        if stripped_line.startswith("tftp-server "):
            tftp_settings.append(stripped_line)

        if stripped_line == "service config":
            tftp_settings.append(stripped_line)

        if stripped_line.startswith("ip tftp source-interface "):
            manual_settings.append(stripped_line)

    return tftp_settings, manual_settings


def check_n21_cisco(config_text):
    # N-21은 불필요한 TFTP 서비스가 활성화되어 있는지 점검한다.
    found_settings = []
    weak_settings = []
    manual_settings = []

    tftp_settings, tftp_manual_settings = find_tftp_settings(config_text)

    if tftp_settings:
        for setting in tftp_settings:
            weak_settings.append(f"TFTP 관련 서비스 설정 확인: {setting}")
    else:
        found_settings.append("TFTP 서버 서비스 설정 없음")

    for setting in tftp_manual_settings:
        manual_settings.append(f"TFTP source-interface 참고 설정: {setting}")

    if weak_settings:
        result = "취약"
    elif manual_settings:
        result = "수동확인"
    else:
        result = "양호"

    return result, found_settings, weak_settings, manual_settings
