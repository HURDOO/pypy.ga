# python-trainer

## 차례

## 1. 프로젝트 동기

## 2. 이론적 배경

## 3. 필요 기능

- 단계별, 수준별 문제 목록
- 문제/입력/출력 설명, 입력/출력 예시, 제출 화면
- 스팸 방지를 위한 로그인 및 회원 기능

## 4. 사이트 구조도

* `/` 메인 페이지
* `/doc?id=###` 설명 페이지
* `/problem?id=###` 문제 페이지
* `/submit?problem_id=###&submit_id=###` 제출 및 정답 페이지

## 5. 구현 방식

### 5-1. 언어 및 프레임워크
- Python(백엔드 프로그래밍 언어): 단기간의 빠른 개발을 위해, 관련 자료가 풍부하고 높은 생산성을 자랑하는 Python 언어를 사용하였습니다. [참고8]
- Django(백엔드 프레임워크): 빠른 개발과 안전한 웹 프레임워크로 알려져 있고, 교내 공학동아리 로델라에서도 자주 이용하는 Django 프레임워크를 사용하였습니다. [참고9]
- Azure SQL Database(데이터베이스): 

### 5-5. 배포 및 웹서버 구동
 서울특별시교육청에서는 관내 학교의 교사 및 학생들에게 Office 365(현 Microsoft 365) 계정을 제공하고 있습니다.[참고1] 학생 정보를 인증하고 동록하면 Office 계정을 제공받는데, 이 계정은 소속 학교의 도메인(@학교.sen.go.kr)을 사용합니다. 또한 Microsoft사의 클라우드 서비스인 Azure[참고2]에서는 학생들에게 교육적 목적으로 1년간 사용 가능한 $100 크레딧(해당 제품에서 실제 재화 대신 사용할 수 있는 가상 재화)을 무료로 제공합니다.[참고3] 학교 도메인을 포함한 Microsoft 계정을 사용함으로써 이러한 교육적 혜택을 누릴 수 있는데, 이 계정은 위의 서울특별시교육청에서 제공해 주는 Office 365 계정으로 대체 가능합니다. 이러한 혜택을 통해 금전적 부담 없이 웹 서버를 구축할 수 있습니다.

 Python 프로젝트를 업로드하면 웹 서버를 구동해주는 Azure App Service를 사용합니다.[참고4] 프로젝트는 Microsoft의 계열사이자 오픈소스 코드 공유 플렛폼인 깃허브[참고5]에 오픈소스(코드 공개 상태)로 업로드되며, https://github.com/HURDOO/python-trainer에서 확인 가능합니다. 이러한 프로젝트는 Github Actions[참고6]를 통해 빌드(작성한 코드를 구동하기 전 필요한 설정 및 작업 수행)하여 Azure App Service에 배포합니다.

 웹 주소는 freenom.com에서 무료로 발급 가능한 도메인 중, Python의 앞 두글자 py를 따와 pypy.ga 도메인을 사용했습니다. DNS 서버는 Azure DNS 영역을 사용합니다.

### 5-4. 계정 시스템
 로그인에는 학교에서 제공해 준 Google 계정(@sonline20.sen.go.kr) 을 사용합니다. 유저는 로그인 버튼을 눌러 구글 로그인 창으로 넘어가게 되고, 구글 서버에서 이메일을 서버로 받아와 도메인이 학교 계정의 도메인(@sonline20.sen.go.kr) 이 맞는지 확인합니다. 확인이 완료되면 세션 ID가 새로고침되며 로그인 상태가 됩니다.


## 6. 구현 방식
### 1) `index/` - 메인 페이지
* `/` - 문제 목록을 로드합니다. 문제 목록이 비어있다면, 문제 목록을 새로 불러옵니다.
![순서도](readme/index.png)

### 2) `account/` - 계정 페이지
* `/account/login` - 구글 로그인 링크를 생성하고, 안내 페이지를 로드합니다.
* `/account/logout` - 로그인 정보를 삭제하고, 메인 화면으로 이동합니다.
* `/account/auth` - 로그인 완료 후 이동되는 페이지로, 구글 서버로 요청을 보내 엑세스 토큰을 요청하고, 해당 토큰을 이용하여 이메일 주소를 받아옵니다. 이메일 주소가 유효하다면 로그인 정보를 저장하고 메인 화면으로 이동하며, 유효하지 않다면 로그인 안내 페이지로 이동합니다.
![순서도](readme/account.png)

### 3) `problem/` - 문제 페이지
* `/problem/<int>` - 해당하는 문제와 코드 에디터 화면을 표시합니다. 이전에 해당 문제에서 제출한 기록이 있다면 해당 제출의 코드를 불러옵니다.


## 참고 문헌

1. https://o365.sen.go.kr/
2. https://azure.microsoft.com/ko-kr/resources/cloud-computing-dictionary/what-is-azure/
3. https://azure.microsoft.com/ko-kr/free/students/
4. https://azure.microsoft.com/ko-kr/services/app-service/
5. https://github.com/about
6. https://docs.github.com/en/actions
7. https://www.djangoproject.com/
8. https://library.gabia.com/contents/9256/
9. https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Introduction