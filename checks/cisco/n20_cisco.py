def find_snmp_lines(config_text):
    # running-config에서 snmp-server로 시작하는 설정을 찾는다.
    snmp_lines = []

    for line in config_text.splitlines():
        stripped_line = line.strip()

        if stripped_line.startswith("snmp-server"):
            snmp_lines.append(stripped_line)

    return snmp_lines


def find_community_lines(snmp_lines):
    # SNMP Community 설정만 분리한다.
    community_lines = []

    for line in snmp_lines:
        if line.startswith("snmp-server community "):
            community_lines.append(line)

    return community_lines


def get_community_permission(line):
    # 예: "snmp-server community kisec123 RO 100"에서 권한 값인 RO를 꺼낸다.
    parts = line.split()

    if len(parts) < 4:
        return None

    return parts[3].upper()


def check_community_permission(line):
    permission = get_community_permission(line)

    if permission == "RO":
        return line, None

    if permission == "RW":
        return None, f"SNMP Community 쓰기 권한 사용: {line}"

    return None, f"SNMP Community 권한 값 확인 불가: {line}"


def check_n20_cisco(config_text):
    # N-20은 SNMP Community 권한이 읽기 전용(RO)으로 설정되어 있는지 점검한다.
    found_settings = []
    weak_settings = []
    manual_settings = []

    snmp_lines = find_snmp_lines(config_text)
    community_lines = find_community_lines(snmp_lines)

    if not snmp_lines:
        found_settings.append("SNMP 서비스 설정 없음")
    elif not community_lines:
        found_settings.append("SNMP Community 설정 없음")
        manual_settings.append("SNMPv3 사용자/그룹 권한 수동확인 필요")
    else:
        for line in community_lines:
            found, weak = check_community_permission(line)

            if found:
                found_settings.append(found)

            if weak:
                weak_settings.append(weak)

    if weak_settings:
        result = "취약"
    elif manual_settings:
        result = "수동확인"
    else:
        result = "양호"

    return result, found_settings, weak_settings, manual_settings
