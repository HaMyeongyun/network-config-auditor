def find_logging_buffered_lines(config_text):
    # running-config에서 logging buffered 설정을 찾는다.
    buffered_lines = []

    for line in config_text.splitlines():
        stripped_line = line.strip()

        if stripped_line.startswith("logging buffered"):
            buffered_lines.append(stripped_line)

    return buffered_lines


def get_buffer_size(line):
    # 예: "logging buffered 16000"에서 버퍼 크기인 16000을 숫자로 꺼낸다.
    # 예: "logging buffered 16000 debugging"처럼 뒤에 로깅 레벨이 붙어도 처리한다.
    parts = line.split()

    if len(parts) < 3:
        return None

    try:
        return int(parts[2])
    except ValueError:
        return None


def check_n13_cisco(config_text):
    # N-13은 Cisco 기준으로 logging buffered 크기가 일반 권장 범위인지 점검한다.
    # 기준: 16000 미만 취약, 16000~32000 양호, 32000 초과 수동확인.
    found_settings = []
    weak_settings = []
    manual_settings = []

    buffered_lines = find_logging_buffered_lines(config_text)

    if not buffered_lines:
        weak_settings.append("logging buffered 설정 없음")
    else:
        for line in buffered_lines:
            buffer_size = get_buffer_size(line)

            if buffer_size is None:
                manual_settings.append(f"로깅 버퍼 크기 값 확인 필요: {line}")
            elif buffer_size < 16000:
                weak_settings.append(f"로깅 버퍼 크기 기준 미달: {line}")
            elif buffer_size <= 32000:
                found_settings.append(line)
            else:
                found_settings.append(line)
                manual_settings.append(
                    f"로깅 버퍼 크기가 일반 권장 범위(16Kbyte~32Kbyte)를 초과함: {line}"
                )
                manual_settings.append("장비 메모리, 로그 발생량, 기관 정책 기준 확인 필요")

    if weak_settings:
        result = "취약"
    elif manual_settings:
        result = "수동확인"
    else:
        result = "양호"

    return result, found_settings, weak_settings, manual_settings
