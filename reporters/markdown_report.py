def add_section(lines, title, items):
    lines.append(f"#### {title}")

    if items:
        lines.append("```text")
        for item in items:
            lines.append(item)
        lines.append("```")
    else:
        lines.append("없음")

    lines.append("")

def make_markdown_report(report_title, section_title, check_results):
    lines = []

    lines.append(f"# {report_title}")
    lines.append("")
    lines.append(f"# {section_title}")
    lines.append("")

    for check in check_results:
        lines.append(f"### {check['code']} {check['title']}")
        lines.append(f"- 점검 결과: **{check['result']}**")
        lines.append("")

        add_section(lines, "확인된 설정", check["found"])
        add_section(lines, "미흡한 설정", check["weak"])
        add_section(lines, "수동확인 필요", check["manual"])

    return "\n".join(lines)
