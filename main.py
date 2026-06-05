from pathlib import Path

from checks.cisco.n01_cisco import check_n01_cisco
from checks.cisco.n02_cisco import check_n02_cisco
from checks.cisco.n03_cisco import check_n03_cisco
from checks.cisco.n04_cisco import check_n04_cisco
from checks.cisco.n05_cisco import check_n05_cisco
from checks.cisco.n06_cisco import check_n06_cisco
from checks.cisco.n07_cisco import check_n07_cisco
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
#-------------------

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

# ---------------------------------------------
    result, found_settings, weak_setting = check_n01_cisco(config_text)

    print("\n[N-01] 비밀번호 설정")
    print(f"점검 결과 {result}")

    print("\n확인된 설정:")
    if found_settings:
        for setting in found_settings:
            if setting.startswith("line "):
                print(setting)
            else:
                print(f"- {setting}")
    else:
        print("- 없음")

    print("\n미흡한 설정")
    if weak_setting:
        for setting in weak_setting:
            print(f"- {setting}")
    else:
        print("- 없음")
#---------------------------------------------
    result, found_settings, weak_setting = check_n02_cisco(config_text)
    print("\n[N-02 비밀번호 복잡성 설정]")
    print(f"점검 결과 {result}")

    print("\n확인된 결과")
    if found_settings:
        for setting in found_settings:
            print(f"- {setting}")
    else:
        print("없음")

    print("\n 미흡한 설정")
    if weak_setting:
        for setting in weak_setting:
            print(f"- {setting}")
    else:
        print("- 없음")
# ---------------------------------------------

    result, found_settings, weak_setting = check_n03_cisco(config_text)
    print("\n[N-03] 암호화된 비밀번호 사용")
    print(f"점검 결과 {result}")

    print("\n확인된 설정")
    if found_settings:
        for setting in found_settings:
            print(f"- {setting}")
    else:
        print("- 없음")

    print("\n미흡한 설정")
    if weak_setting:
        for setting in weak_setting:
            print(f"- {setting}")
    else:
        print("- 없음")

# ---------------------------------------------

    result, found_settings, weak_setting = check_n04_cisco(config_text)
    print("\n[N-04] 계정 잠금 임계값 설정")
    print(f"점검 결과 {result}")

    print("\n확인된 설정")
    if found_settings:
        for setting in found_settings:
            print(f"- {setting}")
    else:
        print("- 없음")

    print("\n미흡한 설정")
    if weak_setting:
        for setting in weak_setting:
            print(f"- {setting}")
    else:
        print("- 없음")

#--------------------------------
    result, found_settings, weak_setting, manual_settings = check_n05_cisco(config_text)
    print("\n[N-05] 사용자·명령어별 권한 수준 설정")
    print(f"점검 결과 {result}")

    print("\n확인된 설정")
    if found_settings:
        for setting in found_settings:
            print(f"- {setting}")
    else:
        print("- 없음")

    print("\n미흡한 설정")
    if weak_setting:
        for setting in weak_setting:
            print(f"- {setting}")
    else:
        print("- 없음")

    print("\n수동확인 필요")
    if manual_settings:
        for setting in manual_settings:
            print(f"- {setting}")
    else:
        print("- 없음")
#---------------------------
    result, found_settings, weak_setting, manual_settings = check_n06_cisco(config_text)
    print("\n[N-06] VTY 접근(ACL) 설정")
    print(f"점검 결과 {result}")

    print("\n확인된 설정")
    if found_settings:
        for setting in found_settings:
            if setting.startswith("line "):
                print(setting)
            else:
                print(f"- {setting}")
    else:
        print("- 없음")

    print("\n미흡한 설정")
    if weak_setting:
        for setting in weak_setting:
            print(f"- {setting}")
    else:
        print("- 없음")

    print("\n미적용 ACL")
    if manual_settings:
        for setting in manual_settings:
            if setting.startswith("미적용"):
                print(setting)
            else:
                print(f"- {setting}")
    else:
        print("- 없음")

#---------------------------
    result, found_settings, weak_setting = check_n07_cisco(config_text)
    print("\n[N-07] Session Timeout 설정")
    print(f"점검 결과 {result}")

    print("\n확인된 설정")
    if found_settings:
        for setting in found_settings:
            if setting.startswith("line "):
                print(setting)
            else:
                print(f"- {setting}")
    else:
        print("- 없음")

    print("\n미흡한 설정")
    if weak_setting:
        for setting in weak_setting:
            print(f"- {setting}")
    else:
        print("- 없음")






    # print("_____ running-config 시작_____")
    # print(config_text)
    # print("_____running-config 끝")









#-----------------------
    checks = [
        ("N-01", "비밀번호 설정", check_n01_cisco),
        ("N-02", "비밀번호 복잡성 설정", check_n02_cisco),
        ("N-03", "암호화된 비밀번호 사용", check_n03_cisco),
        ("N-04", "계정 잠금 임계값 설정", check_n04_cisco),
        ("N-05", "사용자·명령어별 권한 수준 설정", check_n05_cisco),
        ("N-06", "VTY 접근(ACL) 설정", check_n06_cisco),
        ("N-07", "Session Timeout 설정", check_n07_cisco),
    ]

    check_results = []

    for code, title, check_function in checks:
        check_result = check_function(config_text)
        normalized_result = normalize_result(code, title, check_result)
        check_results.append(normalized_result)

    report_text = make_markdown_report(
        "네트워크 장비 점검 보고서",
        "현재 구현 항목: N-01 ~ N-07",
        check_results,
    )

    report_file.write_text(report_text, encoding="utf-8")

    print(f"보고서 생성 완료: {report_file}")

if __name__ == "__main__":
    main()
