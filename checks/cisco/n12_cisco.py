def find_version_lines(config_text):
    # Cisco running-config에서 OS/이미지 버전 근거가 되는 줄을 찾는다.
    version_lines = []

    for line in config_text.splitlines():
        stripped_line = line.strip()

        if stripped_line.startswith("version "):
            version_lines.append(stripped_line)

    return version_lines


def format_running_config_version(line):
    # 예: "version 16.6.4"를 "running-config version: 16.6.4"로 바꾼다.
    parts = line.split(maxsplit=1)

    if len(parts) < 2:
        return "running-config version: 값 확인 불가"

    return f"running-config version: {parts[1]}"


def check_n12_cisco(config_text):
    # N-12는 주기적 보안 패치 및 벤더 권고사항 적용 여부를 점검한다.
    # running-config/show version만으로 패치 적용 여부를 확정할 수 없으므로,
    # 버전 근거가 있으면 인터뷰 필요, 버전 근거가 없으면 버전정보 확인 필요로 분리한다.
    found_settings = []
    weak_settings = []
    manual_settings = []

    version_lines = find_version_lines(config_text)

    if version_lines:
        for line in version_lines:
            found_settings.append(format_running_config_version(line))

        manual_settings.append("show version 정보 제공 여부 확인 필요")
        manual_settings.append("Cisco Software Checker에서 해당 IOS/IOS-XE 버전의 권고사항 확인 필요")
        manual_settings.append("https://sec.cloudapps.cisco.com/security/center/softwarechecker.x")
        manual_settings.append("기관 패치 정책 및 정기 패치 수행 이력 확인 필요")
        manual_settings.append("운영 영향도 검토 및 패치 테스트/백업 수행 여부 확인 필요")
        manual_settings.append("패치 적용 예외 또는 N/A 대상 여부 확인 필요")
        result = "인터뷰 필요"
    else:
        weak_settings.append("장비 OS 버전 정보 없음")
        manual_settings.append("show version 또는 장비 버전 증적 추가 수집 필요")
        manual_settings.append("Cisco Software Checker 확인을 위한 IOS/IOS-XE 버전 정보 필요")
        result = "버전정보 확인 필요"

    return result, found_settings, weak_settings, manual_settings
