# 요구사항 명세서
## 기능적 요구사항

### 1) 회원 가입
- 사용자가 ID 및 PW를 입력 > 데이터 베이스에 등록
- 이미 등록된 ID > 경고창 출력

### 2) 로그인
- ID / PW 입력 여부 확인
- 등록된 멤버인 지 판별
- ID에 해당하는 PW가 올바른 지 확인
- PW에 입력된 값은 "\*"로 출력

### 3) 방 목록 출력
- 데이터 베이스에 등록된 데이터를 사용자 기준에 따라 정렬해 출력
- 기본 정렬은 방 생성 날짜 기준

### 4) 방 생성
- 방 제목을 입력 > 방 별 인식 코드를 난수로 발생
- 특수문자를 입력 > 경고창 출력
- 기존에 있는 방 제목 > 경고창 출력
- 방 제목 길이 20자로 제한
- 방 생성 시 데이터 베이스에 등록

### 5) 방 삭제
- 삭제할 방 클릭 후 삭제 버튼 클릭
- 로그인 된 사용자와 방장 불일치 > 경고창 출력
- 방 인식 코드가 데이터 베이스에 없는 경우 > 경고창 출력
- 삭제 여부를 재확인 > 삭제 또는 취소

### 6) 파일 목록 출력
- 데이터 베이스에 등록된 데이터를 사용자 기준에 따라 정렬해 출력
- 기본 정렬은 파일 업로드 날짜 기준
- 뒤로가기 버튼 클릭 > 방 목록으로 이동

### 7) 파일 업로드
- 사용자가 파일 불러와서 업로드 > 데이터 베이스 등록
- 파일에 접근 권한이 없는 경우 > 경고창 출력
- 파이썬 파일(.py)이 아닌 경우 > 경고창 출력
- 파일 업데이트
  - 로그인 된 사용자와 파일의 소유자가 같고, 파일명이 이전에 등록된 파일명과 같으면 내용만 업데이트
  - 업데이트 여부를 재확인 > 업데이트 또는 취소

### 8) 파일 삭제
- 삭제할 파일 클릭 후 삭제 버튼 클릭
- 로그인 된 사용자와 파일 소유자 불일치 > 경고창 출력
- 파일명이 데이터 베이스에 없는 경우 > 경고창 출력
- 삭제 여부를 재확인 > 삭제 또는 취소

### 9) 파일 내용 열람
- 파이썬 문법 기준으로 하이라이팅된 텍스트 출력
- "좋아요" 버튼 > 파일별 "좋아요" 수 기록
<br/>

## 사용자 인터페이스 요구사항
<img src="https://github.com/dulsik2/SW2_ADproject_ShareCode/blob/master/specification/img/1.jpg?raw=true" width="400px">

>1. ID와 PW를 입력받는 에디트창
>2. 로그인 버튼 > 예외 사항 발생 시 경고창 출력
>3. 회원가입 버튼 > 회원가입 창으로 연결

<br/>

<img src="https://github.com/dulsik2/SW2_ADproject_ShareCode/blob/master/specification/img/2.jpg?raw=true" width="400px">

>1. 사용자가 사용할 ID, PW, 별명을 입력받는 에디트창
>2. 완료 버튼 > 예외 사항 발생 시 경고창 출력

<br/>

<img src="https://github.com/dulsik2/SW2_ADproject_ShareCode/blob/master/specification/img/3.jpg?raw=true" width="400px">

>1. 정렬 기준 콤보 박스와 체크 버튼
>2. 방 타이틀, 파일 수, 업로더 정보, 생성 날짜 표시
>3. 스크롤 바
>4. 삭제할 방 선택 후 방 삭제 버튼 > 삭제 여부 재확인 및 예외에 대한 경고창 출력
>5. 방 만들기 버튼 > 방 생성 창으로 연결

<br/>


<img src="https://github.com/dulsik2/SW2_ADproject_ShareCode/blob/master/specification/img/4.jpg?raw=true" width="400px">

>1. 방 타이틀을 입력받는 에디트창
>2. 완료 버튼 > 예외 사항 발생 시 경고창 출력

<br/>

<img src="https://github.com/dulsik2/SW2_ADproject_ShareCode/blob/master/specification/img/5.jpg?raw=true" width="400px">

>1. 정렬 기준 콤보 박스와 체크 버튼
>2. 파일 이름, "좋아요" 수, 업로더 정보, 생성 날짜 표시
>3. 스크롤 바
>4. 삭제할 파일 선택 후 파일 삭제 버튼 > 삭제 여부 재확인 및 예외에 대한 경고창 출력
>5. 업로드 버튼 > 파일 불러오기 창으로 연결

<br/>

<img src="https://github.com/dulsik2/SW2_ADproject_ShareCode/blob/master/specification/img/6.jpg?raw=true" width="400px">

>1. 파일 불러오기 창

<br/>

<img src="https://github.com/dulsik2/SW2_ADproject_ShareCode/blob/master/specification/img/7.jpg?raw=true" width="400px">

>1. 파일 이름 출력
>2. "좋아요" 버튼
>3. 파이썬 문법 기준으로 하이라이팅된 텍스트 출력

<br/>

## 비기능적 요구사항
1. 이 소프트웨어의 구현에는 Python과 PyQt5, Database(MySQL)를 이용한다.
2. Database는 AWS 서버로 올려서 활용하는 방안을 채택했다.
3. 데이터 과부하를 막기 위해 30일이 지난 데이터를 지운다.