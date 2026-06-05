def find_banner_blocks(config_text):
    # Cisco banner는 "banner login #" 다음 줄부터 종료 문자("#")가 나올 때까지 이어진다.
    lines = config_text.splitlines()
    banner_blocks = []
    current_block = []
    in_banner = False
    end_marker = None

    for line in lines:
        stripped_line = line.strip()

        if stripped_line.startswith("banner login ") or stripped_line.startswith("banner motd "):
            parts = stripped_line.split()
            end_marker = parts[-1] if parts else None
            current_block = [stripped_line]
            in_banner = True
            continue

        if in_banner:
            current_block.append(stripped_line)

            if stripped_line == end_marker:
                banner_blocks.append(current_block)
                current_block = []
                in_banner = False
                end_marker = None

    if current_block:
        banner_blocks.append(current_block)

    return banner_blocks


def check_n10_cisco(config_text):
    # N-10은 Cisco 기준으로 로그인 시 경고 메시지 배너 설정 여부를 점검한다.
    found_settings = []
    weak_settings = []

    banner_blocks = find_banner_blocks(config_text)

    if banner_blocks:
        for banner_block in banner_blocks:
            found_settings.extend(banner_block)
    else:
        weak_settings.append("로그인 경고 배너 설정 없음")

    if weak_settings:
        result = "취약"
    else:
        result = "양호"

    return result, found_settings, weak_settings
