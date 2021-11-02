# Asignment1-TW-JW-YY
원티드x위코드 백엔드 프리온보딩 과제1
- 과제 출제 기업 정보
  - 기업명 : 에이모
  - [에이모 사이트](https://aimmo.co.kr/)
  - [wanted 채용공고 링크](https://www.wanted.co.kr/wd/16937)

## Members
- 김태우 고유영, 박지원

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
    - 대댓글 pagination
- 게시글 읽힘 수
    - 같은 User가 게시글을 읽는 경우 count 수 증가하면 안 됨
- Rest API 설계
- Unit Test
- 1000만건 이상의 데이터를 넣고 성능테스트 진행 결과 필요


## 사용 기술 및 tools
> - Back-End :  <img src="https://img.shields.io/badge/Python 3.8-3776AB?style=for-the-badge&logo=Python&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Django 3.2-092E20?style=for-the-badge&logo=Django&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/mongodb 5.0.3-1b9e41?style=for-the-badge&logo=Mongodb&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/PyJWT 2.1-000000?style=for-the-badge&logo=JsonWebTokens&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Bcrypt 3.2-338000?style=for-the-badge&logo=PyJWT&logoColor=white"/>
> - Deploy : <img src="https://img.shields.io/badge/AWS_EC2-232F3E?style=for-the-badge&logo=Amazon&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Docker-0052CC?style=for-the-badge&logo=Docker&logoColor=white"/>
> - ETC :  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=Github&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=Postman&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Trello-0052CC?style=for-the-badge&logo=Trello&logoColor=white"/>

## 모델링

## API

## 구현 기능

## API TEST 방법

## 설치 및 실행 방법
###  Local 개발 및 테스트용
1. miniconda를 설치한다. ([https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html))
2. 해당프로젝트를 clone 하고, 프로젝트 폴더로 들어간다.
    
    ```bash
    git clone https://github.com/Wanted-Preonboarding-Backend-1st-G5/Assignment1-TW-JW-YY
    cd Assignment1-TW-JW-YY
    ```
    
3. .dockerenv.local_dev 파일을 만들어서 안에 다음과 같은 내용을 입력한다. manage.py와 같은 폴더에 생성한다.
    
    ```text
    # .dockerenv.local_dev
    DJANGO_SECRECT_KEY='django프로젝트 SECRECT_KEY'
    ```

4. docker-compose를 통해서 db와 서버를 실행시킨다.
    
    ```bash
    docker-compose -f docker-compose-local-dev.yml up
    ```
5. 만약 백그라운드에서 실행하고 싶을 시 `-d` 옵션을 추가한다.
    ```bash
    docker-compose -f docker-compose-local-dev.yml up -d
    ```

## 폴더 구조
```bash
.
└── REAMEME.md
```

## TIL정리 (Blog)
- 김태우 :
- 고유영 :
- 박지원 :