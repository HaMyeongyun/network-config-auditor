REQUIRED_DENY_RULES = [
    "deny ip 0.0.0.0 0.255.255.255 any",
    "deny ip 10.0.0.0 0.255.255.255 any",
    "deny ip 127.0.0.0 0.255.255.255 any",
    "deny ip 169.254.0.0 0.0.255.255 any",
    "deny ip 172.16.0.0 0.15.255.255 any",
    "deny ip 192.0.2.0 0.0.0.255 any",
    "deny ip 192.168.0.0 0.0.255.255 any",
    "deny ip 224.0.0.0 15.255.255.255 any",
]


def find_numbered_acl_rules(config_text):
    # numbered ACL을 ACL 번호별로 모은다.
    acl_rules = {}

    for line in config_text.splitlines():
        stripped_line = line.strip()
        parts = stripped_line.split(maxsplit=2)

        if stripped_line.startswith("access-list ") and len(parts) == 3:
            acl_number = parts[1]
            acl_rule = parts[2]

            if acl_number not in acl_rules:
                acl_rules[acl_number] = []

            acl_rules[acl_number].append(acl_rule)

    return acl_rules


def find_best_matching_acl(acl_rules):
    # 필수 deny 규칙을 가장 많이 포함한 ACL을 찾는다.
    best_acl_number = None
    best_found_rules = []
    best_missing_rules = REQUIRED_DENY_RULES[:]

    for acl_number, rules in acl_rules.items():
        found_rules = []
        missing_rules = []

        for required_rule in REQUIRED_DENY_RULES:
            if required_rule in rules:
                found_rules.append(required_rule)
            else:
                missing_rules.append(required_rule)

        if len(found_rules) > len(best_found_rules):
            best_acl_number = acl_number
            best_found_rules = found_rules
            best_missing_rules = missing_rules

    return best_acl_number, best_found_rules, best_missing_rules


def get_config_blocks(config_text, block_prefix):
    blocks = []
    current_block = []

    for line in config_text.splitlines():
        stripped_line = line.strip()

        if stripped_line.startswith(block_prefix):
            if current_block:
                blocks.append(current_block)

            current_block = [stripped_line]
            continue

        if current_block:
            if line.startswith(" ") or line.startswith("\t"):
                current_block.append(stripped_line)
            else:
                blocks.append(current_block)
                current_block = []

    if current_block:
        blocks.append(current_block)

    return blocks


def find_acl_interface_applications(config_text, acl_number):
    # 인터페이스에 ip access-group <ACL> in/out으로 적용된 설정을 찾는다.
    applications = []
    interface_blocks = get_config_blocks(config_text, "interface ")

    for block in interface_blocks:
        interface_name = block[0]

        for line in block[1:]:
            if line == f"ip access-group {acl_number} in":
                applications.append(f"{interface_name} - {line}")

            if line == f"ip access-group {acl_number} out":
                applications.append(f"{interface_name} - {line}")

    return applications


def check_n22_cisco(config_text):
    # N-22는 Spoofing 방지를 위한 특수 용도 Source IP 대역 차단 ACL을 점검한다.
    found_settings = []
    weak_settings = []
    manual_settings = []

    acl_rules = find_numbered_acl_rules(config_text)
    acl_number, found_rules, missing_rules = find_best_matching_acl(acl_rules)

    if acl_number is None:
        weak_settings.append("Spoofing 방지 Source IP 차단 ACL 설정 없음")
    else:
        found_settings.append(f"Spoofing 방지 ACL: {acl_number}")

        for rule in found_rules:
            found_settings.append(f"access-list {acl_number} {rule}")

        for rule in missing_rules:
            weak_settings.append(f"누락된 차단 규칙: access-list {acl_number} {rule}")

        applications = find_acl_interface_applications(config_text, acl_number)

        if applications:
            found_settings.extend(applications)
        else:
            weak_settings.append(f"ACL {acl_number} 인터페이스 적용 설정 없음")

    if weak_settings:
        result = "취약"
    else:
        result = "양호"

    return result, found_settings, weak_settings, manual_settings
