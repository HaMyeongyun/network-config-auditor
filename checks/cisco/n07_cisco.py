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


def find_exec_timeout_line(block_lines):
    # line 블록 안에서 exec-timeout 설정을 찾는다.
    for line in block_lines:
        if line.startswith("exec-timeout"):
            return line

    return None


def get_exec_timeout_seconds(line):
    # 예: "exec-timeout 5 0"은 5분 0초이므로 전체 초 단위인 300을 반환한다.
    # Cisco 형식: exec-timeout <minutes> <seconds>
    parts = line.split()

    if len(parts) < 2:
        return None

    try:
        minutes = int(parts[1])

        if len(parts) >= 3:
            seconds = int(parts[2])
        else:
            seconds = 0

        return minutes * 60 + seconds
    except ValueError:
        return None


def check_timeout_block(block_lines):
    block_header = block_lines[0]
    timeout_line = find_exec_timeout_line(block_lines)

    if timeout_line is None:
        return None, f"{block_header} Session Timeout 미설정"

    timeout_seconds = get_exec_timeout_seconds(timeout_line)

    if timeout_seconds is None:
        return None, f"{block_header} Session Timeout 값 확인 불가: {timeout_line}"

    if timeout_seconds == 0:
        return None, f"{block_header} Session Timeout 비활성화 설정: {timeout_line}"

    if timeout_seconds <= 600:
        return [block_header, timeout_line], None

    return None, f"{block_header} Session Timeout 10분 초과 설정: {timeout_line}"


def check_n07_cisco(config_text):
    # N-07은 Cisco 기준으로 Session Timeout이 10분 이하인지 점검한다.
    found_settings = []
    weak_settings = []

    target_blocks = []
    target_blocks.extend(get_config_blocks(config_text, "line con"))
    target_blocks.extend(get_config_blocks(config_text, "line console"))
    target_blocks.extend(get_config_blocks(config_text, "line vty"))
    target_blocks.extend(get_config_blocks(config_text, "line aux"))

    if not target_blocks:
        weak_settings.append("line console/vty/aux 설정 블록 없음")
    else:
        for block_lines in target_blocks:
            found, weak = check_timeout_block(block_lines)

            if found:
                found_settings.extend(found)

            if weak:
                weak_settings.append(weak)

    if weak_settings:
        result = "취약"
    else:
        result = "양호"

    return result, found_settings, weak_settings
