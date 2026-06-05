# 네트워크 장비 점검 보고서

# 현재 구현 항목: N-01 ~ N-11

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
- 점검 결과: **양호**

#### 확인된 설정
```text
security passwords min-length 8
```

#### 미흡한 설정
없음

#### 수동확인 필요
없음

### N-03 암호화된 비밀번호 사용
- 점검 결과: **양호**

#### 확인된 설정
```text
service password-encryption
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
- 점검 결과: **양호**

#### 확인된 설정
```text
logging 192.168.3.1
```

#### 미흡한 설정
없음

#### 수동확인 필요
```text
logging userinfo
logging trap debugging
```
