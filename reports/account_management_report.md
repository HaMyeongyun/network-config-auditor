# 네트워크 장비 점검 보고서

# 01. 계정 관리

### N-01 비밀번호 설정
- 점검 결과: **취약**

#### 확인된 설정
```text
enable secret 5 $1$mERr$OSspVDKdDcSbol7vzHaH3.
username admin secret 0 $1$mERr$OSspVDKdDcSbol7vzHaH3.
username kisec password 7 082A455D0C1A544541
username kisec2 password 0 kisec123
username kisec2 password 0 kisec123
username test password 1 082A455D0C1A544541
username kisec3 privilege 15 secret 5 $1$mERr$OSspVDKdDcSbol7vzHaH3.
line console 0
login local
line aux 0
no exec
```

#### 미흡한 설정
```text
vty 패스워드 미설정
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
- 점검 결과: **취약**

#### 확인된 설정
```text
enable secret 5 $1$mERr$OSspVDKdDcSbol7vzHaH3.
username kisec password 7 082A455D0C1A544541
username kisec3 privilege 15 secret 5 $1$mERr$OSspVDKdDcSbol7vzHaH3.
```

#### 미흡한 설정
```text
평문 또는 암호화 미흡 비밀번호 설정: username admin secret 0 $1$mERr$OSspVDKdDcSbol7vzHaH3.
평문 또는 암호화 미흡 비밀번호 설정: username kisec2 password 0 kisec123
평문 또는 암호화 미흡 비밀번호 설정: username kisec2 password 0 kisec123
평문 또는 암호화 미흡 비밀번호 설정: username test password 1 082A455D0C1A544541
```

#### 수동확인 필요
없음

### N-04 계정 잠금 임계값 설정
- 점검 결과: **양호**

#### 확인된 설정
```text
login block-for 120 attempts 3 within 60
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
username admin secret 0 $1$mERr$OSspVDKdDcSbol7vzHaH3.
username kisec password 7 082A455D0C1A544541
username kisec2 password 0 kisec123
username kisec2 password 0 kisec123
username test password 1 082A455D0C1A544541
username kisec3 privilege 15 secret 5 $1$mERr$OSspVDKdDcSbol7vzHaH3.
```
