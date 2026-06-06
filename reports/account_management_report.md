# 네트워크 장비 점검 보고서

# 현재 구현 항목: N-01 ~ N-23

### N-01 비밀번호 설정
- 점검 결과: **취약**

#### 확인된 설정
```text
enable secret 5 $1$mERr$OSspVDKdDcSbol7vzHaH3.
username kisec secret 5 $1$mERr$OSspVDKdDcSbol7vzHaH3.
username kisec123 privilege 15 secret 5 $1$mERr$OSspVDKdDcSbol7vzHaH3.
username kisec2 secret 5 $1$mERr$OSspVDKdDcSbol7vzHaH3.
username test secret 5 $1$mERr$OSspVDKdDcSbol7vzHaH3.
line vty 0 4
password 7 082A455D0C1A544541
login local
line vty 5 14
password 7 082A455D0C1A544541
login local
line aux 0
password 7 082A455D0C1A544541
```

#### 미흡한 설정
```text
console 패스워드 미설정
```

#### 수동확인 필요
없음

### N-02 비밀번호 복잡성 설정
- 점검 결과: **취약**

#### 확인된 설정
없음

#### 미흡한 설정
```text
비밀번호 최소 길이 정책 미설정
```

#### 수동확인 필요
없음

### N-03 암호화된 비밀번호 사용
- 점검 결과: **양호**

#### 확인된 설정
```text
enable secret 5 $1$mERr$OSspVDKdDcSbol7vzHaH3.
username kisec secret 5 $1$mERr$OSspVDKdDcSbol7vzHaH3.
username kisec123 privilege 15 secret 5 $1$mERr$OSspVDKdDcSbol7vzHaH3.
username kisec2 secret 5 $1$mERr$OSspVDKdDcSbol7vzHaH3.
username test secret 5 $1$mERr$OSspVDKdDcSbol7vzHaH3.
password 7 082A455D0C1A544541
password 7 082A455D0C1A544541
password 7 082A455D0C1A544541
password 7 082A455D0C1A544541
```

#### 미흡한 설정
없음

#### 수동확인 필요
없음

### N-04 계정 잠금 임계값 설정
- 점검 결과: **양호**

#### 확인된 설정
```text
login block-for 300 attempts 5 within 60
```

#### 미흡한 설정
없음

#### 수동확인 필요
없음

### N-05 사용자·명령어별 권한 수준 설정
- 점검 결과: **취약**

#### 확인된 설정
```text
privilege exec level 15 connect
privilege exec level 15 telnet
privilege exec level 15 show ip access-list
privilege exec level 15 show logging
```

#### 미흡한 설정
```text
rlogin 명령어 level 15 미설정
```

#### 수동확인 필요
```text
username kisec secret 5 $1$mERr$OSspVDKdDcSbol7vzHaH3.
username kisec123 privilege 15 secret 5 $1$mERr$OSspVDKdDcSbol7vzHaH3.
username kisec2 secret 5 $1$mERr$OSspVDKdDcSbol7vzHaH3.
username test secret 5 $1$mERr$OSspVDKdDcSbol7vzHaH3.
```

### N-06 VTY 접근(ACL) 설정
- 점검 결과: **취약**

#### 확인된 설정
```text
line vty 0 4
access-class 1 in
line vty 5 14
access-class 2 in
```

#### 미흡한 설정
```text
access-class 1 in 참조 ACL 설정 없음
access-class 2 in 참조 ACL 설정 없음
```

#### 수동확인 필요
```text
미적용 access-list 3
access-list 3 permit host 20.0.0.20
access-list 3 deny any
미적용 access-list 100
access-list 100 permit udp host 10.10.10.10 any eq snmp
access-list 100 permit udp host 10.10.10.20 any eq snmp
access-list 100 deny ip any any
미적용 access-list 101
access-list 101 deny ip 0.0.0.0 0.255.255.255 any
access-list 101 deny ip 10.0.0.0 0.255.255.255 any
access-list 101 deny ip 127.0.0.0 0.255.255.255 any
access-list 101 deny ip 169.254.0.0 0.0.255.255 any
access-list 101 deny ip 172.16.0.0 0.15.255.255 any
access-list 101 deny ip 192.0.2.0 0.0.0.255 any
access-list 101 deny ip 192.168.0.0 0.0.255.255 any
access-list 101 deny ip 224.0.0.0 15.255.255.255 any
access-list 101 permit ip any any
```

### N-07 Session Timeout 설정
- 점검 결과: **취약**

#### 확인된 설정
```text
line con 0
exec-timeout 5 0
line vty 5 14
exec-timeout 5 0
line aux 0
exec-timeout 0 1
```

#### 미흡한 설정
```text
line vty 0 4 Session Timeout 비활성화 설정: exec-timeout 0 0
```

#### 수동확인 필요
없음

### N-08 VTY 접속 시 안전한 프로토콜 사용
- 점검 결과: **취약**

#### 확인된 설정
```text
ip ssh version 2
ip ssh authentication-retries 5
ip ssh time-out 60
ip domain-name kisec.com
line vty 0 4
transport input ssh
```

#### 미흡한 설정
```text
line vty 5 14 transport input 설정 없음
```

#### 수동확인 필요
없음

### N-09 불필요한 보조 입출력 포트 사용 금지
- 점검 결과: **수동확인**

#### 확인된 설정
```text
line aux 0
exec-timeout 0 1
```

#### 미흡한 설정
없음

#### 수동확인 필요
```text
line aux 0 차단 설정과 접속 허용 설정이 함께 존재
password 7 082A455D0C1A544541
login
```

### N-10 로그인 시 경고 메시지 설정
- 점검 결과: **양호**

#### 확인된 설정
```text
banner motd #
kisec nonoonononono
#
```

#### 미흡한 설정
없음

#### 수동확인 필요
없음

### N-11 원격 로그서버 사용
- 점검 결과: **취약**

#### 확인된 설정
없음

#### 미흡한 설정
```text
원격 로그서버 IP 설정 없음
```

#### 수동확인 필요
```text
logging userinfo
logging buffered 18000
logging trap debugging
```

### N-12 주기적 보안 패치 및 벤더 권고사항 적용
- 점검 결과: **인터뷰 필요**

#### 확인된 설정
```text
running-config version: 15.4
```

#### 미흡한 설정
없음

#### 수동확인 필요
```text
show version 정보 제공 여부 확인 필요
Cisco Software Checker에서 해당 IOS/IOS-XE 버전의 권고사항 확인 필요
https://sec.cloudapps.cisco.com/security/center/softwarechecker.x
기관 패치 정책 및 정기 패치 수행 이력 확인 필요
운영 영향도 검토 및 패치 테스트/백업 수행 여부 확인 필요
패치 적용 예외 또는 N/A 대상 여부 확인 필요
```

### N-13 로깅 버퍼 크기 설정
- 점검 결과: **양호**

#### 확인된 설정
```text
logging buffered 18000
```

#### 미흡한 설정
없음

#### 수동확인 필요
없음

### N-14 정책에 따른 로깅 설정
- 점검 결과: **인터뷰 필요**

#### 확인된 설정
없음

#### 미흡한 설정
```text
running-config 내 logging server 설정 없음
```

#### 수동확인 필요
```text
show logging 출력 정보 확인 필요
기관 로깅 정책 문서 확인 필요
정책에 따른 로그 레벨, 보관 대상, 보관 기간, 원격 전송 여부 확인 필요
보안사고 분석 및 법적 증적 확보 기준 충족 여부 확인 필요
```

### N-15 NTP 및 시각 동기화 설정
- 점검 결과: **양호**

#### 확인된 설정
```text
ntp server 192.168.0.123
clock timezone KST 9
```

#### 미흡한 설정
없음

#### 수동확인 필요
```text
show ntp status 또는 show clock으로 실제 시각 동기화 상태 확인 필요
NTP 서버 접근 가능 여부 및 시간 차이 확인 필요
기관 표준 시간대 및 시각 동기화 정책 기준 확인 필요
```

### N-16 Timestamp 로그 설정
- 점검 결과: **양호**

#### 확인된 설정
```text
service timestamps log datetime msec
```

#### 미흡한 설정
없음

#### 수동확인 필요
없음

### N-17 SNMP 서비스 확인
- 점검 결과: **취약**

#### 확인된 설정
없음

#### 미흡한 설정
```text
SNMP v1/v2c 계열 설정 확인: snmp-server community kise@c123 Rw 100
```

#### 수동확인 필요
```text
SNMP 서비스 사용 필요성 확인 필요
사용하지 않는 SNMP 서비스라면 비활성화 필요
SNMP Community String, ACL, 권한 설정은 N-18~N-20에서 추가 점검 필요
```

### N-18 SNMP Community String 복잡성 설정
- 점검 결과: **양호**

#### 확인된 설정
```text
snmp-server community kise@c123 Rw 100
```

#### 미흡한 설정
없음

#### 수동확인 필요
없음

### N-19 SNMP ACL 설정
- 점검 결과: **양호**

#### 확인된 설정
```text
snmp-server community kise@c123 Rw 100
SNMP ACL: 100
access-list 100 permit udp host 10.10.10.10 any eq snmp
access-list 100 permit udp host 10.10.10.20 any eq snmp
access-list 100 deny ip any any
```

#### 미흡한 설정
없음

#### 수동확인 필요
없음

### N-20 SNMP Community 권한 설정
- 점검 결과: **취약**

#### 확인된 설정
없음

#### 미흡한 설정
```text
SNMP Community 쓰기 권한 사용: snmp-server community kise@c123 Rw 100
```

#### 수동확인 필요
없음

### N-21 TFTP 서비스 차단
- 점검 결과: **양호**

#### 확인된 설정
```text
TFTP 서버 서비스 설정 없음
```

#### 미흡한 설정
없음

#### 수동확인 필요
없음

### N-22 Spoofing 방지 필터링 적용
- 점검 결과: **양호**

#### 확인된 설정
```text
Spoofing 방지 ACL: 101
access-list 101 deny ip 0.0.0.0 0.255.255.255 any
access-list 101 deny ip 10.0.0.0 0.255.255.255 any
access-list 101 deny ip 127.0.0.0 0.255.255.255 any
access-list 101 deny ip 169.254.0.0 0.0.255.255 any
access-list 101 deny ip 172.16.0.0 0.15.255.255 any
access-list 101 deny ip 192.0.2.0 0.0.0.255 any
access-list 101 deny ip 192.168.0.0 0.0.255.255 any
access-list 101 deny ip 224.0.0.0 15.255.255.255 any
interface GigabitEthernet0/0/1 - ip access-group 101 in
```

#### 미흡한 설정
없음

#### 수동확인 필요
없음

### N-23 DDoS 공격 방어 설정
- 점검 결과: **수동확인**

#### 확인된 설정
```text
logging userinfo
logging buffered 18000
ip flow-export version 9
ip access-list extended sl_def_acl
access-list 3 permit host 20.0.0.20
access-list 3 deny any
access-list 100 permit udp host 10.10.10.10 any eq snmp
access-list 100 permit udp host 10.10.10.20 any eq snmp
access-list 100 deny ip any any
access-list 101 deny ip 0.0.0.0 0.255.255.255 any
access-list 101 deny ip 10.0.0.0 0.255.255.255 any
access-list 101 deny ip 127.0.0.0 0.255.255.255 any
access-list 101 deny ip 169.254.0.0 0.0.255.255 any
access-list 101 deny ip 172.16.0.0 0.15.255.255 any
access-list 101 deny ip 192.0.2.0 0.0.0.255 any
access-list 101 deny ip 192.168.0.0 0.0.255.255 any
access-list 101 deny ip 224.0.0.0 15.255.255.255 any
access-list 101 permit ip any any
logging trap debugging
```

#### 미흡한 설정
없음

#### 수동확인 필요
```text
DDoS 대응 정책 및 절차 문서 확인 필요
DDoS 방어 서비스 또는 보안관제 연동 여부 확인 필요
최근 DDoS 대응 훈련, 점검, 대응 이력 확인 필요
임계치 기반 탐지, 알림, 우회, 차단 절차 확인 필요
ISP, 보안관제, 내부 담당자 연락체계 확인 필요
```
