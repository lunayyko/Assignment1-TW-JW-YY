# Asignment1-TW-JW-YY
원티드x위코드 백엔드 프리온보딩 과제1
- 과제 출제 기업 정보
  - 기업명 : 에이모
  - [에이모 사이트](https://aimmo.co.kr/)
  - [wanted 채용공고 링크](https://www.wanted.co.kr/wd/16937)

## Members
|이름   |github                   |담당 기능|
|-------|-------------------------|--------------------|
|김태우 |[jotasic](https://github.com/jotasic)     | 개발 및 배포 환경 설정, 게시글 CRUD   |
|고유영 |[lunayyko](https://github.com/lunayyko)   | DB Modeling, 댓글 대댓글 CRUD   |
|박지원 |[jiwon5304](https://github.com/jiwon5304) | DB Modeling, 회원가입, 로그인, 댓글 대댓글 pagination, postman api 작성   |


## 과제 내용
> 아래 요구사항에 맞춰 게시판 Restfull API를 개발합니다.
- 에이모 선호 기술스택: python flask, mashmallow, mongoengine
- 필수 사용 데이터베이스: mongodb

### [필수 포함 사항]
- Swagger나 Postman을 이용하여 API 테스트 가능하도록 구현
- READ.ME 작성
    - 프로젝트 빌드, 자세한 실행 방법 명시
    - 구현 방법과 이유에 대한 간략한 설명
    - 완료된 시스템이 배포된 서버의 주소
    - Swagger나 Postman을 통한 API 테스트할때 필요한 상세 방법
    - 해당 과제를 진행하면서 회고 내용 블로그 포스팅

### [개발 요구사항]
- 원티드 지원 과제 내용 포함 (기본적인 게시판 글쓰기)
- 게시글 카테고리
- 게시글 검색
- 대댓글(1 depth)
    - 댓글 및 대댓글 pagination
- 게시글 읽힘 수
    - 같은 User가 게시글을 읽는 경우 count 수 증가하면 안 됨
- Rest API 설계
- Unit Test
- 1000만건 이상의 데이터를 넣고 성능테스트 진행 결과 필요


## 사용 기술 및 tools
> - Back-End :  <img src="https://img.shields.io/badge/Python 3.8-3776AB?style=for-the-badge&logo=Python&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Django 3.2-092E20?style=for-the-badge&logo=Django&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/mongodb 5.0-1b9e41?style=for-the-badge&logo=Mongodb&logoColor=white"/>
> - Deploy : <img src="https://img.shields.io/badge/AWS_EC2-232F3E?style=for-the-badge&logo=Amazon&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Docker-0052CC?style=for-the-badge&logo=Docker&logoColor=white"/>
> - ETC :  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=Github&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=Postman&logoColor=white"/>

## 모델링
![5 drawio](https://user-images.githubusercontent.com/8315252/139969615-38f01f08-cc1c-427e-87a6-09671525525b.png)

## API
[링크-postman document](https://documenter.getpostman.com/view/16042359/UVBzmpLX)

## 구현 기능
### 회원가입, 로그인
- 회원가입시 password 같은 민감정보는 단방향 해쉬 알고리즘인 `bcrypt`를 이용해서 암호화 하여 database에 저장하였습니다.
- 로그인이 성공적으로 완료되면, user정보를 토큰으로 반환할때, 양방향 해쉬 알고리즘인 `JWT`를 사용해서 응답을 하였습니다.

### 게시글 CRUD
- 게시글의 모든 조작 및 조회는 로그인시에(header에 token이 있는 상태) 가능하도록 하였습니다.
- 글 삭제, 수정은 해당글을 작성한 user만 가능하도록 하였습니다.
- 게시글 상세 보기의 경우는 우선 글을 조회한 user가 해당글을 처음 보왔을 경우만 해당글의 조회수를 1 증가 시키도록 하였습니다. 해당 기능구현을 위해서 특정 user가 특정 게시물을 읽은 정보는 AccessLog라는 model에 저장하도록 하였습니다.
- 게시글 조회(List)의 경우 query string을 이용해서 pagination, 게시글 검색, 카테고리 필터링, 정렬 등의 기능을 구현하였습니다.

### 댓글 대댓글 CRUD
- parent_comment 필드를 이용해서 부모 댓글의 id를 기억하도록 하였습니다. 만약 댓글일 경우는 parent_comment의 값이 Null이 되고, 대댓글의 경우는 parent_comment값이 부모 댓글의 id가 되도록 하였습니다.
- 댓글과 대댓글을 같은 API를 사용하도록 구현하였으며 방법은 query string를 이용해서 parent_id가 0일경우는 해당 게시글의 댓글을 조회하도록 하였고, parent_id가 1이상일 경우는 해당 게시글의 해당 부모 댓글의 id가 같은 댓글들을 필터링하여, 대댓글을 조회하도록 하였습니다.
- 댓글과 대댓글 모두 pagination이 가능하도록 구현하였습니다.

### Djongo - Mongodb connector
- [링크](https://github.com/nesdis/djongo)
- Django에서 기본적으로 제공하는 Database는 Mongodb가 포함되어 있지 않습니다. Django의 장점인 ORM을 이용하면 추후 Database가 RDBMS로 변경시에서 쉽게 대응 할 수 있다고 판단하여, Mongodb기반의 ORM을 작성할 수 있도록 해주는 Djongo를 사용하여 Mongodb와 연결하였습니다.

### Docker
- 팀원들의 빠른 개발환경 셋팅을 위해서 로컬 개발용과 배포용 docker-compose 파일을 만들어서 적용하였습니다.
- 개발용 환경을 구축했을 시 장점은 팀원들의 개발환경 셋팅시간을 줄여줘서 구현에 더 집중 할 수 있습니다.
- 배포용 환경을 구축했을 시에는 일일이 셋팅을 한다고하면, 아무래도 서버와 로컬간의 OS 같은 환경에 차이로 인해서 시간를 낭비 할 수도 있으며 특히, 배포시마다 이러한 상황이 반복될 수 있다는 것인데, docker를 통해서 이러한 시간낭비를 줄 일 수 있다는 장점이 있습니다. 

## API TEST 방법
1. 우측 링크를 클릭해서 postman으로 들어갑니다. [링크](https://www.postman.com/wecode-21-1st-kaka0/workspace/assignment1-tw-jw-yy/overview)
2. 정의된 SERVER_URL이 올바른지 확인 합니다. (18.188.189.173:8000)
<img width="743" alt="스크린샷 2021-11-03 오전 12 23 05" src="https://user-images.githubusercontent.com/8219812/139912122-87d71d1d-d318-4057-8d76-f7311952ea75.png">

3. 정의된 회원가입, 로그인 요청을 이용해서 access_token을 획득합니다.

4. 각 요청에 header 부분에 Authorization 항목에 획득한 access_token을 입력하여 요청을 진행합니다. 회원가입, 로그인을 제외한 요청에는 access_token이 필요합니다.
<img width="1255" alt="스크린샷 2021-11-03 오전 1 58 17" src="https://user-images.githubusercontent.com/8219812/139912164-a5f49a32-5128-4902-a9d9-03dfa6a94672.png">

5. 만약 Send버튼이 비활성화가 될 시 fork를 이용해서 해당 postman project를 복사해서 시도하길 바랍니다.
![image](https://user-images.githubusercontent.com/8219812/139912241-d6cb5831-23e8-4cbb-a747-f52c42601098.png)

## 설치 및 실행 방법
###  Local 개발 및 테스트용
1. miniconda를 설치한다. ([https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html))
2. 해당프로젝트를 clone 하고, 프로젝트 폴더로 들어간다.
    ```bash
    git clone https://github.com/Wanted-Preonboarding-Backend-1st-G5/Assignment1-TW-JW-YY
    cd Assignment1-TW-JW-YY
    ```
3. 가상 환경을 만들고 프로젝트에 사용한 python package를 받는다.
    ```bash
    conda create --name Assignment1-TW-JW-YY python=3.8
    conda actvate Assignment1-TW-JW-YY
    pip install -r requirements.txt
    ```

4. .dockerenv.local_dev 파일을 만들어서 안에 다음과 같은 내용을 입력한다. manage.py와 같은 폴더에 생성한다.
    
    ```text
    # .dockerenv.local_dev

    DJANGO_SECRECT_KEY='django프로젝트 SECRECT_KEY'
    ```

5. docker-compose를 통해서 db와 서버를 실행시킨다.
    
    ```bash
    docker-compose -f docker-compose-local-dev.yml up
    ```
6. 만약 백그라운드에서 실행하고 싶을 시 `-d` 옵션을 추가한다.
    ```bash
    docker-compose -f docker-compose-local-dev.yml up -d
    ```

###  배포용 
1. 해당프로젝트를 clone 하고, 프로젝트 폴더로 들어간다.
    
    ```bash
    git clone https://github.com/Wanted-Preonboarding-Backend-1st-G5/Assignment1-TW-JW-YY
    cd Assignment1-TW-JW-YY
    ```
2. .dockerenv.deploy 파일을 만들어서 안에 다음과 같은 내용을 입력한다. manage.py와 같은 폴더에 생성한다.
    
    ```text
    # .dockerenv.deploy

    DJANGO_SECRECT_KEY='django프로젝트 SECRECT_KEY'
    DB_PORT=DB포트번호
    DB_NAME='DB이름'
    ```
3. docker-compose를 통해서 db와 서버를 실행시킨다.
    
    ```bash
    docker-compose -f docker-compose-deploy.yml up
    ```
4. 만약 백그라운드에서 실행하고 싶을 시 `-d` 옵션을 추가한다.
    ```bash
    docker-compose -f docker-compose-deploy.yml up -d
    ```

## 폴더 구조
```bash
.
├── Dockerfile-deploy
├── Dockerfile-local-dev
├── README.md
├── aimmo
│   ├── asgi.py
│   ├── settings
│   │   ├── base.py
│   │   └── local_dev.py
│   ├── urls.py
│   └── wsgi.py
├── core
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── docker-compose-deploy.yml
├── docker-compose-local-dev.yml
├── manage.py
├── posts
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── requirements.txt
└── users
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── decorators.py
    ├── migrations
    ├── models.py
    ├── tests.py
    ├── urls.py
    └── views.py

```

## TIL정리 (Blog)
[고유영 : 루나의 기술블로그 - 원티드 x 위코드 프리온보딩 과제1 Aimmo(몽고디비대댓글)](https://lunayyko.github.io/wecode/2021/11/03/wantedxwecode-1-aimmo/)  

# Reference
이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 aimmo에서 출제한 과제를 기반으로 만들었습니다.
