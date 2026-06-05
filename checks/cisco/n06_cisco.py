def get_config_blocks(config_text, block_start):
    # 같은 종류의 설정 블록이 여러 개 있을 때 모두 찾는다.
    # 예: "line vty 0 4", "line vty 5 15"를 각각 블록으로 모은다.
    lines = config_text.splitlines()
    blocks = []
    current_block = []
    in_block = False

    for line in lines:
        stripped_line = line.strip()

        if stripped_line.startswith(block_start):
            if current_block:
                blocks.append(current_block)

            in_block = True
            current_block = [stripped_line]
            continue

        if in_block:
            if line and not line.startswith(" "):
                blocks.append(current_block)
                current_block = []
                in_block = False
                continue

            current_block.append(stripped_line)

    if current_block:
        blocks.append(current_block)

    return blocks


def find_access_class_lines(block_lines):
    # VTY 블록 안에서 access-class 설정을 찾는다.
    matched_lines = []

    for line in block_lines:
        if line.startswith("access-class"):
            matched_lines.append(line)

    return matched_lines


def get_acl_name_from_access_class(line):
    # 예: "access-class 1 in"에서 ACL 번호/이름인 "1"을 꺼낸다.
    parts = line.split()

    if len(parts) < 2:
        return None

    return parts[1]


def find_numbered_acl_lines(config_text, acl_name):
    # 예: access-class 1 in 이면 "access-list 1 ..." 설정을 모두 찾는다.
    matched_lines = []
    prefix = f"access-list {acl_name} "

    for line in config_text.splitlines():
        stripped_line = line.strip()

        if stripped_line.startswith(prefix):
            matched_lines.append(stripped_line)

    return matched_lines


def find_all_numbered_acl_lines(config_text):
    # running-config에 있는 numbered access-list를 ACL 번호별로 모은다.
    acl_map = {}

    for line in config_text.splitlines():
        stripped_line = line.strip()

        if not stripped_line.startswith("access-list "):
            continue

        parts = stripped_line.split()

        if len(parts) < 2:
            continue

        acl_name = parts[1]

        if acl_name not in acl_map:
            acl_map[acl_name] = []

        acl_map[acl_name].append(stripped_line)

    return acl_map


def find_named_acl_block(config_text, acl_name):
    # 예: access-class MGMT in 처럼 이름 기반 ACL을 참조하는 경우
    # "ip access-list standard MGMT" 또는 "ip access-list extended MGMT" 블록을 찾는다.
    lines = config_text.splitlines()
    block_lines = []
    in_block = False

    for line in lines:
        stripped_line = line.strip()

        if (
            stripped_line == f"ip access-list standard {acl_name}"
            or stripped_line == f"ip access-list extended {acl_name}"
        ):
            in_block = True
            block_lines.append(stripped_line)
            continue

        if in_block:
            if line and not line.startswith(" "):
                break

            block_lines.append(stripped_line)

    return block_lines


def find_referenced_acl_lines(config_text, access_class_line):
    acl_name = get_acl_name_from_access_class(access_class_line)

    if acl_name is None:
        return []

    numbered_acl_lines = find_numbered_acl_lines(config_text, acl_name)
    if numbered_acl_lines:
        return numbered_acl_lines

    return find_named_acl_block(config_text, acl_name)


def check_n06_cisco(config_text):
    # N-06은 Cisco 기준으로 VTY 접근 제어 ACL(access-class) 설정 여부를 점검한다.
    found_settings = []
    weak_settings = []
    manual_settings = []
    applied_acl_names = []

    vty_blocks = get_config_blocks(config_text, "line vty")

    if not vty_blocks:
        weak_settings.append("line vty 설정 블록 없음")
    else:
        for vty_block in vty_blocks:
            vty_header = vty_block[0]
            access_class_lines = find_access_class_lines(vty_block)

            if access_class_lines:
                found_settings.append(vty_header)
                found_settings.extend(access_class_lines)

                for access_class_line in access_class_lines:
                    acl_name = get_acl_name_from_access_class(access_class_line)
                    if acl_name:
                        applied_acl_names.append(acl_name)

                    acl_lines = find_referenced_acl_lines(config_text, access_class_line)

                    if acl_lines:
                        found_settings.extend(acl_lines)
                    else:
                        weak_settings.append(f"{access_class_line} 참조 ACL 설정 없음")
            else:
                weak_settings.append(f"{vty_header} 접근 제어 ACL 미설정")

    numbered_acl_map = find_all_numbered_acl_lines(config_text)

    for acl_name, acl_lines in numbered_acl_map.items():
        if acl_name not in applied_acl_names:
            manual_settings.append(f"미적용 access-list {acl_name}")
            manual_settings.extend(acl_lines)

    if weak_settings:
        result = "취약"
    else:
        result = "양호"

    return result, found_settings, weak_settings, manual_settings
