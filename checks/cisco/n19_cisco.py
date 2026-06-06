def find_snmp_community_lines(config_text):
    # SNMP Community 설정을 찾는다.
    community_lines = []

    for line in config_text.splitlines():
        stripped_line = line.strip()

        if stripped_line.startswith("snmp-server community "):
            community_lines.append(stripped_line)

    return community_lines


def find_all_acl_names(config_text):
    # numbered ACL과 named ACL 이름을 모두 수집한다.
    acl_names = set()

    for line in config_text.splitlines():
        stripped_line = line.strip()
        parts = stripped_line.split()

        if stripped_line.startswith("access-list ") and len(parts) >= 2:
            acl_names.add(parts[1])

        if stripped_line.startswith("ip access-list ") and len(parts) >= 4:
            acl_names.add(parts[3])

    return acl_names


def find_numbered_acl_lines(config_text, acl_name):
    # 예: ACL 10이면 "access-list 10 ..." 설정을 모두 찾는다.
    acl_lines = []
    prefix = f"access-list {acl_name} "

    for line in config_text.splitlines():
        stripped_line = line.strip()

        if stripped_line.startswith(prefix):
            acl_lines.append(stripped_line)

    return acl_lines


def find_named_acl_block(config_text, acl_name):
    # 예: "ip access-list standard SNMP_ACL" 블록을 찾는다.
    acl_block = []
    in_block = False

    for line in config_text.splitlines():
        stripped_line = line.strip()

        if (
            stripped_line == f"ip access-list standard {acl_name}"
            or stripped_line == f"ip access-list extended {acl_name}"
        ):
            in_block = True
            acl_block.append(stripped_line)
            continue

        if in_block:
            if line and not line.startswith(" "):
                break

            acl_block.append(stripped_line)

    return acl_block


def find_acl_lines(config_text, acl_name):
    numbered_acl_lines = find_numbered_acl_lines(config_text, acl_name)

    if numbered_acl_lines:
        return numbered_acl_lines

    return find_named_acl_block(config_text, acl_name)


def get_snmp_acl_name(line):
    # 예: "snmp-server community kisec123 RO 10"에서 ACL 값인 10을 꺼낸다.
    # Cisco community 형식은 보통 "snmp-server community <string> <RO/RW> [ACL]"이다.
    parts = line.split()

    if len(parts) < 5:
        return None

    return parts[4]


def check_n19_cisco(config_text):
    # N-19는 SNMP Community에 접근 제어 ACL이 적용되어 있는지 점검한다.
    found_settings = []
    weak_settings = []
    manual_settings = []

    community_lines = find_snmp_community_lines(config_text)
    acl_names = find_all_acl_names(config_text)

    if not community_lines:
        found_settings.append("SNMP Community 설정 없음")
        manual_settings.append("SNMPv3 사용 여부 또는 SNMP 서비스 비활성화 여부 확인 필요")
    else:
        for line in community_lines:
            acl_name = get_snmp_acl_name(line)

            if acl_name is None:
                weak_settings.append(f"SNMP Community ACL 미설정: {line}")
            elif acl_name in acl_names:
                acl_lines = find_acl_lines(config_text, acl_name)
                found_settings.append(line)
                found_settings.append(f"SNMP ACL: {acl_name}")
                found_settings.extend(acl_lines)
            else:
                weak_settings.append(f"SNMP Community 참조 ACL 정의 없음: {line}")

    if weak_settings:
        result = "취약"
    elif manual_settings:
        result = "수동확인"
    else:
        result = "양호"

    return result, found_settings, weak_settings, manual_settings
