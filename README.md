# Network Config Auditor

Cisco running-config 기반 네트워크 장비 보안 점검 자동화 프로젝트입니다.

현재 구현 범위는 주요정보통신기반시설 네트워크 장비 점검 항목 중 `01. 계정 관리` 파트입니다.

## 현재 점검 항목

- `N-01` 비밀번호 설정
- `N-02` 비밀번호 복잡성 설정
- `N-03` 암호화된 비밀번호 사용
- `N-04` 계정 잠금 임계값 설정
- `N-05` 사용자·명령어별 권한 수준 설정

## 실행 방법

```bash
python main.py
```

실행하면 `samples/running-config.txt`를 읽고, 결과 보고서를 `reports/account_management_report.md`에 생성합니다.

## 폴더 구조

```text
checks/cisco/       Cisco 점검 항목별 로직
reporters/          보고서 생성 로직
samples/            테스트용 running-config
reports/            생성된 보고서와 학습 자료
scripts/            보조 스크립트
```

