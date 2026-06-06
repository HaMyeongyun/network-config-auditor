from pathlib import Path

from checks.cisco.n01_cisco import check_n01_cisco
from checks.cisco.n02_cisco import check_n02_cisco
from checks.cisco.n03_cisco import check_n03_cisco
from checks.cisco.n04_cisco import check_n04_cisco
from checks.cisco.n05_cisco import check_n05_cisco
from checks.cisco.n06_cisco import check_n06_cisco
from checks.cisco.n07_cisco import check_n07_cisco
from checks.cisco.n08_cisco import check_n08_cisco
from checks.cisco.n09_cisco import check_n09_cisco
from checks.cisco.n10_cisco import check_n10_cisco
from checks.cisco.n11_cisco import check_n11_cisco
from checks.cisco.n12_cisco import check_n12_cisco
from checks.cisco.n13_cisco import check_n13_cisco
from checks.cisco.n14_cisco import check_n14_cisco
from checks.cisco.n15_cisco import check_n15_cisco
from checks.cisco.n16_cisco import check_n16_cisco
from checks.cisco.n17_cisco import check_n17_cisco
from checks.cisco.n18_cisco import check_n18_cisco
from checks.cisco.n19_cisco import check_n19_cisco
from checks.cisco.n20_cisco import check_n20_cisco
from checks.cisco.n21_cisco import check_n21_cisco
from checks.cisco.n22_cisco import check_n22_cisco
from checks.cisco.n23_cisco import check_n23_cisco

from reporters.console_report import print_check_result
from reporters.markdown_report import make_markdown_report


def normalize_result(code, title, check_result):
    if len(check_result) == 3:
        result, found_settings, weak_settings = check_result
        manual_settings = []
    else:
        result, found_settings, weak_settings, manual_settings = check_result

    return {
        "code": code,
        "title": title,
        "result": result,
        "found": found_settings,
        "weak": weak_settings,
        "manual": manual_settings,
    }


def run_checks(config_text, checks):
    check_results = []

    for code, title, check_function in checks:
        check_result = check_function(config_text)
        normalized_result = normalize_result(code, title, check_result)
        check_results.append(normalized_result)

    return check_results


def main():
    print("네트워크 장비 점검 자동화 시작")

    project_root = Path(__file__).resolve().parent
    config_file = project_root / "samples" / "running-config.txt"
    reports_dir = project_root / "reports"
    report_file = reports_dir / "account_management_report.md"

    reports_dir.mkdir(exist_ok=True)

    print(f"프로젝트 경로: {project_root}")
    print(f"설정 파일 경로: {config_file}")
    print(f"파일 존재 여부: {config_file.exists()}")

    config_text = config_file.read_text(encoding="utf-8")

    checks = [
        ("N-01", "비밀번호 설정", check_n01_cisco),
        ("N-02", "비밀번호 복잡성 설정", check_n02_cisco),
        ("N-03", "암호화된 비밀번호 사용", check_n03_cisco),
        ("N-04", "계정 잠금 임계값 설정", check_n04_cisco),
        ("N-05", "사용자·명령어별 권한 수준 설정", check_n05_cisco),
        ("N-06", "VTY 접근(ACL) 설정", check_n06_cisco),
        ("N-07", "Session Timeout 설정", check_n07_cisco),
        ("N-08", "VTY 접속 시 안전한 프로토콜 사용", check_n08_cisco),
        ("N-09", "불필요한 보조 입출력 포트 사용 금지", check_n09_cisco),
        ("N-10", "로그인 시 경고 메시지 설정", check_n10_cisco),
        ("N-11", "원격 로그서버 사용", check_n11_cisco),
        ("N-12", "주기적 보안 패치 및 벤더 권고사항 적용", check_n12_cisco),
        ("N-13", "로깅 버퍼 크기 설정", check_n13_cisco),
        ("N-14", "정책에 따른 로깅 설정", check_n14_cisco),
        ("N-15", "NTP 및 시각 동기화 설정", check_n15_cisco),
        ("N-16", "Timestamp 로그 설정", check_n16_cisco),
        ("N-17", "SNMP 서비스 확인", check_n17_cisco),
        ("N-18", "SNMP Community String 복잡성 설정", check_n18_cisco),
        ("N-19", "SNMP ACL 설정", check_n19_cisco),
        ("N-20", "SNMP Community 권한 설정", check_n20_cisco),
        ("N-21", "TFTP 서비스 차단", check_n21_cisco),
        ("N-22", "Spoofing 방지 필터링 적용", check_n22_cisco),
        ("N-23", "DDoS 공격 방어 설정", check_n23_cisco),
    ]

    check_results = run_checks(config_text, checks)

    for check_result in check_results:
        print_check_result(check_result)

    report_text = make_markdown_report(
        "네트워크 장비 점검 보고서",
        "현재 구현 항목: N-01 ~ N-23",
        check_results,
    )

    report_file.write_text(report_text, encoding="utf-8")

    print(f"\n보고서 생성 완료: {report_file}")


if __name__ == "__main__":
    main()
