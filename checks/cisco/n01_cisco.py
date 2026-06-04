def get_config_block(config_text, block_start):
    # running-config를 줄 단위로 나눠서 특정 설정 블록을 찾는다.
    # 예: "line vty"를 찾으면 다음 상위 설정이 나오기 전까지의 줄을 모은다.
    lines = config_text.splitlines()
    block_lines = []
    in_block = False

    for line in lines:
        # Cisco 설정은 하위 명령 앞에 공백이 붙기 때문에 비교용으로 공백을 제거한다.
        stripped_line = line.strip()

        if stripped_line.startswith(block_start):
            in_block = True
            block_lines.append(stripped_line)
            continue

        if in_block:
            # 블록 안에 있다가 공백 없이 시작하는 새 설정이 나오면 현재 블록이 끝난 것이다.
            if line and not line.startswith(" "):
                break

            block_lines.append(stripped_line)

    return block_lines


def find_lines(config_text, keywords):
    # 전체 설정에서 특정 키워드로 시작하는 줄을 찾는다.
    # 예: "enable secret", "username" 같은 전역 설정을 찾을 때 사용한다.
    matches_lines = []

    for line in config_text.splitlines():
        stripped_line = line.strip()

        for keyword in keywords:
            if stripped_line.startswith(keyword):
                matches_lines.append(stripped_line)
                break
    return matches_lines


def find_auth_lines_in_block(block_lines):
    # line console/vty/aux 블록 안에서 인증 또는 비활성화 관련 설정을 찾는다.
    auth_keywords = [
        "password",
        "login local",
        "login authentication",
        "no exec",
    ]

    matches_lines = []

    for line in block_lines:
        for keyword in auth_keywords:
            if line.startswith(keyword):
                matches_lines.append(line)
                break

    return matches_lines


def check_n01_cisco(config_text):
    # N-01은 Cisco running-config 기준으로 비밀번호/인증 설정 여부를 점검한다.
    # found_settings에는 확인된 실제 설정 줄을 넣고, weak_settings에는 미흡한 항목을 넣는다.
    found_settings = []
    weak_settings = []

    # enable secret/password는 관리자 권한 모드 진입 비밀번호 설정이다.
    enable_lines = find_lines(config_text, ["enable secret", "enable password"])
    if enable_lines:
        found_settings.extend(enable_lines)
    else:
        weak_settings.append("enable 비밀번호 미설정")

    # username 설정 중 secret/password가 포함된 계정만 비밀번호 설정 계정으로 판단한다.
    user_lines = find_lines(config_text, ["username"])
    password_user_lines = []

    for line in user_lines:
        if "secret" in line or "password" in line:
            password_user_lines.append(line)
    if password_user_lines:
        found_settings.extend(password_user_lines)
    else:
        weak_settings.append("사용자 계정 패스워드 미설정")

    # 콘솔 접속 구간에서 password/login local/login authentication 설정이 있는지 확인한다.
    console_block = get_config_block(config_text, "line console")
    console_auth_lines = find_auth_lines_in_block(console_block)

    if console_auth_lines:
        found_settings.append("line console 0")
        found_settings.extend(console_auth_lines)
    else:
        weak_settings.append("console 패스워드 미설정")

    # VTY는 Telnet/SSH 같은 원격 터미널 접속 구간이다.
    vty_block = get_config_block(config_text, "line vty")
    vty_auth_lines = find_auth_lines_in_block(vty_block)

    if vty_auth_lines:
        found_settings.append("line vty 0 4")
        found_settings.extend(vty_auth_lines)
    else:
        weak_settings.append("vty 패스워드 미설정")

    # AUX 포트는 사용하지 않으면 no exec로 비활성화되어 있어도 보호 설정으로 본다.
    aux_block = get_config_block(config_text, "line aux")
    aux_auth_lines = find_auth_lines_in_block(aux_block)

    if aux_auth_lines:
        found_settings.append("line aux 0")
        found_settings.extend(aux_auth_lines)
    else:
        weak_settings.append("aux 패스워드 미설정")

    # 미흡한 설정이 하나라도 있으면 전체 판정은 취약으로 둔다.
    if weak_settings:
        result = "취약"
    else:
        result = "양호"

    return result, found_settings, weak_settings
