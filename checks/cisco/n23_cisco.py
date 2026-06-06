DDOS_RELATED_PREFIXES = [
    "ip flow-export",
    "ip flow-cache",
    "ip route-cache flow",
    "logging ",
    "snmp-server enable traps",
    "access-list ",
    "ip access-list ",
    "class-map ",
    "policy-map ",
    "service-policy ",
    "control-plane",
    "storm-control ",
    "rate-limit ",
    "police ",
]


def is_ddos_related_line(line):
    # running-config에서 DDoS 대응 확인에 참고할 수 있는 설정을 찾는다.
    for prefix in DDOS_RELATED_PREFIXES:
        if line.startswith(prefix):
            return True

    return False


def find_ddos_related_settings(config_text):
    related_settings = []

    for line in config_text.splitlines():
        stripped_line = line.strip()

        if is_ddos_related_line(stripped_line):
            related_settings.append(stripped_line)

    return related_settings


def check_n23_cisco(config_text):
    # N-23은 running-config만으로 DDoS 대응 체계의 최종 양호/취약 판단이 어렵다.
    # 관련 설정을 증적으로 수집하고, 정책/관제/훈련 이력은 수동확인 대상으로 출력한다.
    found_settings = []
    weak_settings = []
    manual_settings = []

    related_settings = find_ddos_related_settings(config_text)

    if related_settings:
        found_settings.extend(related_settings)
    else:
        weak_settings.append("running-config 내 DDoS 대응 관련 참고 설정 없음")

    manual_settings.append("DDoS 대응 정책 및 절차 문서 확인 필요")
    manual_settings.append("DDoS 방어 서비스 또는 보안관제 연동 여부 확인 필요")
    manual_settings.append("최근 DDoS 대응 훈련, 점검, 대응 이력 확인 필요")
    manual_settings.append("임계치 기반 탐지, 알림, 우회, 차단 절차 확인 필요")
    manual_settings.append("ISP, 보안관제, 내부 담당자 연락체계 확인 필요")

    return "수동확인", found_settings, weak_settings, manual_settings
