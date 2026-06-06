def find_snmp_lines(config_text):
    # running-config에서 snmp-server로 시작하는 설정을 찾는다.
    snmp_lines = []

    for line in config_text.splitlines():
        stripped_line = line.strip()

        if stripped_line.startswith("snmp-server"):
            snmp_lines.append(stripped_line)

    return snmp_lines


def find_community_lines(snmp_lines):
    # SNMP Community String 설정만 분리한다.
    community_lines = []

    for line in snmp_lines:
        if line.startswith("snmp-server community "):
            community_lines.append(line)

    return community_lines


def get_community_string(line):
    # 예: "snmp-server community kisec123 RO"에서 community 값인 kisec123을 꺼낸다.
    parts = line.split()

    if len(parts) < 3:
        return None

    return parts[2]


def count_character_types(value):
    # Community String에 포함된 문자 종류 수를 계산한다.
    type_count = 0

    if any(char.islower() for char in value):
        type_count += 1

    if any(char.isupper() for char in value):
        type_count += 1

    if any(char.isdigit() for char in value):
        type_count += 1

    if any(not char.isalnum() for char in value):
        type_count += 1

    return type_count


def check_community_complexity(line):
    community = get_community_string(line)

    if community is None:
        return None, f"SNMP Community String 값 확인 불가: {line}"

    if community.lower() in ["public", "private"]:
        return None, f"기본 SNMP Community String 사용: {line}"

    if len(community) < 8:
        return None, f"SNMP Community String 길이 기준 미달: {line}"

    if count_character_types(community) < 3:
        return None, f"SNMP Community String 문자 조합 기준 미달: {line}"

    return line, None


def check_n18_cisco(config_text):
    # N-18은 SNMP 서비스가 비활성화되어 있거나,
    # SNMP Community String이 8자리 이상이고 대문자/소문자/숫자/특수문자 중
    # 3종류 이상을 조합했는지 점검한다.
    found_settings = []
    weak_settings = []
    manual_settings = []

    snmp_lines = find_snmp_lines(config_text)
    community_lines = find_community_lines(snmp_lines)

    if not snmp_lines:
        found_settings.append("SNMP 서비스 설정 없음")
    elif not community_lines:
        manual_settings.append("SNMP Community String 설정 없음")
        manual_settings.append("SNMPv3 사용자 기반 인증 사용 여부 확인 필요")
    else:
        for line in community_lines:
            found, weak = check_community_complexity(line)

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
