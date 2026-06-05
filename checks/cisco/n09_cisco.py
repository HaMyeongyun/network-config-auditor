def get_config_blocks(config_text, block_start):
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


def find_aux_block_settings(block_lines):
    secure_lines = []
    risk_lines = []

    secure_keywords = [
        "no password",
        "transport input none",
        "no exec",
        "exec-timeout 0 1",
    ]

    for line in block_lines:
        for keyword in secure_keywords:
            if line == keyword:
                secure_lines.append(line)
                break

        if line.startswith("password"):
            risk_lines.append(line)

        if line == "login" or line.startswith("login "):
            risk_lines.append(line)

    return secure_lines, risk_lines


def check_n09_cisco(config_text):
    found_settings = []
    weak_settings = []
    manual_settings = []

    aux_blocks = get_config_blocks(config_text, "line aux")

    if not aux_blocks:
        manual_settings.append("line aux 설정 블록 없음")
    else:
        for aux_block in aux_blocks:
            aux_header = aux_block[0]
            secure_lines, risk_lines = find_aux_block_settings(aux_block)

            if secure_lines:
                found_settings.append(aux_header)
                found_settings.extend(secure_lines)

                if risk_lines:
                    manual_settings.append(f"{aux_header} 차단 설정과 접속 허용 설정이 함께 존재")
                    manual_settings.extend(risk_lines)
            else:
                weak_settings.append(aux_header)

                if risk_lines:
                    weak_settings.extend(risk_lines)
                else:
                    weak_settings.append("AUX 포트 차단 설정 없음")

    if weak_settings:
        result = "취약"
    elif manual_settings:
        result = "수동확인"
    else:
        result = "양호"

    return result, found_settings, weak_settings, manual_settings