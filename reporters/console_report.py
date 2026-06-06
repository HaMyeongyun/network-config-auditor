def print_setting_list(title, settings):
    print(f"{title}:")

    if settings:
        for setting in settings:
            if setting.startswith("line "):
                print(setting)
            elif setting.startswith("미적용"):
                print(setting)
            else:
                print(f"- {setting}")
    else:
        print("- 없음")

def print_check_result(check_result):
    print(f"\n[{check_result['code']}] {check_result['title']}")
    print(f"점검 결과: {check_result['result']}")

    print_setting_list("확인된 설정", check_result["found"])
    print_setting_list("미흡한 설정", check_result["weak"])
    print_setting_list("수동확인 필요", check_result["manual"])
