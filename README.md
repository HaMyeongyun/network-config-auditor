# Network Config Auditor

Cisco `running-config` 기반 네트워크 장비 보안 점검 자동화 프로젝트입니다.

현재는 주요정보통신기반시설 네트워크 장비 점검 항목 중 Cisco 기준 `N-01`부터 `N-20`까지의 1차 점검 로직을 구현했습니다.

## 구현 범위

### 01. 계정 관리

- `N-01` 비밀번호 설정
- `N-02` 비밀번호 복잡성 설정
- `N-03` 암호화된 비밀번호 사용
- `N-04` 계정 잠금 임계값 설정
- `N-05` 사용자·명령어별 권한 수준 설정

### 02. 접근 관리

- `N-06` VTY 접근 ACL 설정
- `N-07` Session Timeout 설정
- `N-08` VTY 접속 시 안전한 프로토콜 사용
- `N-09` 불필요한 보조 입출력 포트 사용 금지
- `N-10` 로그인 시 경고 메시지 설정
- `N-11` 원격 로그서버 사용

### 03. 패치 및 로그 관리

- `N-12` 주기적 보안 패치 및 벤더 권고사항 적용
- `N-13` 로깅 버퍼 크기 설정
- `N-14` 정책에 따른 로깅 설정
- `N-15` NTP 및 시각 동기화 설정
- `N-16` Timestamp 로그 설정

### 04. SNMP 관리

- `N-17` SNMP 서비스 확인
- `N-18` SNMP Community String 복잡성 설정
- `N-19` SNMP ACL 설정
- `N-20` SNMP Community 권한 설정

## 점검 방식

이 도구는 제출받은 Cisco `running-config` 내용을 기준으로 설정 존재 여부와 일부 정책값을 자동 점검합니다.

- 자동 판정 결과: `양호`, `취약`, `수동확인`
- 증적 출력: 확인된 설정, 미흡한 설정, 수동확인 필요 항목
- 보고서 출력: Markdown 형식

일부 항목은 설정 파일만으로 최종 판단이 어렵기 때문에 수동확인 대상으로 분리합니다. 예를 들어 사용자 계정별 실제 업무 권한, 로깅 세부 정책, 미적용 ACL 등은 컨설턴트 검토가 필요합니다.

## 실행 방법

```bash
python main.py
```

기본 입력 파일:

```text
samples/running-config.txt
```

실행 결과 보고서:

```text
reports/account_management_report.md
```

## 폴더 구조

```text
checks/cisco/       Cisco 점검 항목별 로직
reporters/          콘솔 및 Markdown 보고서 생성 로직
samples/            테스트용 running-config
reports/            생성된 보고서와 학습 자료
scripts/            보조 스크립트
main.py             점검 실행 진입점
```

## 개발 메모

- `main.py`는 점검 항목 목록을 정의하고 각 점검 함수를 실행합니다.
- `reporters/console_report.py`는 터미널 출력 형식을 담당합니다.
- `reporters/markdown_report.py`는 Markdown 보고서 생성을 담당합니다.
- 각 점검 항목은 `checks/cisco/nXX_cisco.py` 파일로 분리되어 있습니다.

다음 구현 예정 항목은 `N-21`입니다.
