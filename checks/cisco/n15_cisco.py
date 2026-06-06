def find_time_sync_lines(config_text):
    # NTP와 시간대 관련 설정을 찾는다.
    ntp_server_lines = []
    other_time_lines = []

    for line in config_text.splitlines():
        stripped_line = line.strip()

        if stripped_line.startswith("ntp server"):
            ntp_server_lines.append(stripped_line)
        elif (
            stripped_line.startswith("ntp source")
            or stripped_line.startswith("ntp authenticate")
            or stripped_line.startswith("ntp trusted-key")
            or stripped_line.startswith("ntp authentication-key")
            or stripped_line.startswith("clock timezone")
        ):
            other_time_lines.append(stripped_line)

    return ntp_server_lines, other_time_lines


def check_n15_cisco(config_text):
    # N-15는 Cisco 기준으로 NTP 서버 설정 존재 여부를 점검한다.
    # 실제 동기화 상태는 show ntp status/show clock 확인이 필요하므로 수동확인으로 분리한다.
    found_settings = []
    weak_settings = []
    manual_settings = []

    ntp_server_lines, other_time_lines = find_time_sync_lines(config_text)

    if ntp_server_lines:
        found_settings.extend(ntp_server_lines)
    else:
        weak_settings.append("NTP 서버 설정 없음")

    if other_time_lines:
        found_settings.extend(other_time_lines)

    manual_settings.append("show ntp status 또는 show clock으로 실제 시각 동기화 상태 확인 필요")
    manual_settings.append("NTP 서버 접근 가능 여부 및 시간 차이 확인 필요")
    manual_settings.append("기관 표준 시간대 및 시각 동기화 정책 기준 확인 필요")

    if weak_settings:
        result = "취약"
    else:
        result = "양호"

    return result, found_settings, weak_settings, manual_settings
