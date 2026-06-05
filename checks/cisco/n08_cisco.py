def get_config_blocks(config_text, block_start):
    # 같은 종류의 설정 블록이 여러 개 있을 때 모두 찾는다.
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


def get_ssh_version(line):
    # 예: "ip ssh version 2"에서 마지막 값인 2를 숫자로 꺼낸다.
    parts = line.split()

    if not parts:
        return None

    try:
        return int(parts[-1])
    except ValueError:
        return None


def find_transport_input_line(block_lines):
    # VTY 블록 안에서 transport input 설정을 찾는다.
    for line in block_lines:
        if line.startswith("transport input"):
            return line

    return None


def check_ssh_global_settings(config_text):
    # SSH 전역 설정을 점검한다. SSH version은 2 이상이어야 양호로 본다.
    found_settings = []
    weak_settings = []

    version_lines = find_lines(config_text, ["ip ssh version"])

    if not version_lines:
        weak_settings.append("ip ssh version 설정 없음")
    else:
        for line in version_lines:
            ssh_version = get_ssh_version(line)

            if ssh_version is None:
                weak_settings.append(f"SSH version 값 확인 불가: {line}")
            elif ssh_version >= 2:
                found_settings.append(line)
            else:
                weak_settings.append(f"SSH version 기준 미달: {line}")

    required_keywords = [
        "ip ssh authentication-retries",
        "ip ssh time-out",
        "ip domain-name",
    ]

    for keyword in required_keywords:
        matched_lines = find_lines(config_text, [keyword])

        if matched_lines:
            found_settings.extend(matched_lines)
        else:
            weak_settings.append(f"{keyword} 설정 없음")

    return found_settings, weak_settings


def check_vty_transport_settings(config_text):
    # 모든 VTY 블록에서 SSH만 허용하는지 점검한다.
    found_settings = []
    weak_settings = []
    manual_settings = []

    vty_blocks = get_config_blocks(config_text, "line vty")

    if not vty_blocks:
        weak_settings.append("line vty 설정 블록 없음")
        return found_settings, weak_settings, manual_settings

    for vty_block in vty_blocks:
        vty_header = vty_block[0]
        transport_line = find_transport_input_line(vty_block)

        if transport_line is None:
            weak_settings.append(f"{vty_header} transport input 설정 없음")
            continue

        if transport_line == "transport input ssh":
            found_settings.append(vty_header)
            found_settings.append(transport_line)
        elif transport_line == "transport input none":
            manual_settings.append(f"{vty_header} 원격 접속 차단 설정 확인 필요: {transport_line}")
        elif "telnet" in transport_line or "all" in transport_line:
            weak_settings.append(f"{vty_header} 안전하지 않은 프로토콜 허용: {transport_line}")
        else:
            weak_settings.append(f"{vty_header} SSH 전용 접속 설정 아님: {transport_line}")

    return found_settings, weak_settings, manual_settings


def check_n08_cisco(config_text):
    # N-08은 Cisco 기준으로 SSH 전역 설정과 VTY SSH 전용 접속 설정 여부를 점검한다.
    found_settings = []
    weak_settings = []
    manual_settings = []

    ssh_found, ssh_weak = check_ssh_global_settings(config_text)
    vty_found, vty_weak, vty_manual = check_vty_transport_settings(config_text)

    found_settings.extend(ssh_found)
    found_settings.extend(vty_found)

    weak_settings.extend(ssh_weak)
    weak_settings.extend(vty_weak)

    manual_settings.extend(vty_manual)

    if weak_settings:
        result = "취약"
    elif manual_settings:
        result = "수동확인"
    else:
        result = "양호"

    return result, found_settings, weak_settings, manual_settings
