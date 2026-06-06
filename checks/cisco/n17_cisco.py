def find_snmp_lines(config_text):
    # running-config에서 snmp-server로 시작하는 설정을 찾는다.
    snmp_lines = []

    for line in config_text.splitlines():
        stripped_line = line.strip()

        if stripped_line.startswith("snmp-server"):
            snmp_lines.append(stripped_line)

    return snmp_lines


def is_snmp_v3_line(line):
    # Cisco SNMPv3 설정은 보통 user/group 설정에 v3가 포함된다.
    return (
        line.startswith("snmp-server user ") and " v3 " in line
    ) or (
        line.startswith("snmp-server group ") and " v3 " in line
    )


def is_snmp_v1_v2_line(line):
    # community 기반 SNMP는 일반적으로 v1/v2c 계열로 판단한다.
    if line.startswith("snmp-server community "):
        return True

    if " version 1 " in line or " version 2c " in line:
        return True

    return False


def check_n17_cisco(config_text):
    # N-17은 SNMP 서비스 사용 여부와 버전을 확인한다.
    # SNMP 미사용은 양호, SNMPv3 사용은 수동확인, v1/v2c 계열 사용은 취약으로 판단한다.
    found_settings = []
    weak_settings = []
    manual_settings = []

    snmp_lines = find_snmp_lines(config_text)

    if not snmp_lines:
        found_settings.append("SNMP 서비스 설정 없음")
        return "양호", found_settings, weak_settings, manual_settings

    for line in snmp_lines:
        if is_snmp_v3_line(line):
            manual_settings.append(f"SNMPv3 설정 확인: {line}")
        elif is_snmp_v1_v2_line(line):
            weak_settings.append(f"SNMP v1/v2c 계열 설정 확인: {line}")
        else:
            manual_settings.append(line)

    manual_settings.append("SNMP 서비스 사용 필요성 확인 필요")
    manual_settings.append("사용하지 않는 SNMP 서비스라면 비활성화 필요")
    manual_settings.append("SNMP Community String, ACL, 권한 설정은 N-18~N-20에서 추가 점검 필요")

    if weak_settings:
        result = "취약"
    elif manual_settings:
        result = "수동확인"
    else:
        result = "양호"

    return result, found_settings, weak_settings, manual_settings
