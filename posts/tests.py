import jwt, bcrypt, datetime
from unittest import mock

from django.test import TestCase, Client

from users.models  import User
from      .models  import Post, Category, Comment
from django.conf   import settings

class CommentViewTest(TestCase):
    maxDiff = None

    def setUp(self):
        self.test_user = User.objects.create(
            id=1,
            name="지원",
            email="jiwon@mint.com",
            password="abcde12345@",
        )

        Category.objects.create(
            id=1,
            name="위코드"
        )
    
        Post.objects.create(
            id=1,
            user=User.objects.get(id=1),
            subject="제목1",
            content="내용1",
            viewcount = 0,
            category = Category.objects.get(id=1)
        )
        
        self.mocked_date_time = datetime.datetime(2021,1,1,0,0,0)

        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=self.mocked_date_time)):
            Comment.objects.create(
                id=1,
                user=User.objects.get(id=1),
                post=Post.objects.get(id=1),
                parent_comment_id=None,
                content = "댓글1"
            )

            Comment.objects.create(
                id=2,
                user=User.objects.get(id=1),
                post=Post.objects.get(id=1),
                parent_comment_id=None,
                content = "댓글2"
            )

            Comment.objects.create(
                id=3,
                user=User.objects.get(id=1),
                post=Post.objects.get(id=1),
                parent_comment_id=None,
                content = "댓글3"
            )

            Comment.objects.create(
                id=4,
                user=User.objects.get(id=1),
                post=Post.objects.get(id=1),
                parent_comment_id=None,
                content = "댓글4"
            )

            Comment.objects.create(
                id=5,
                user=User.objects.get(id=1),
                post=Post.objects.get(id=1),
                parent_comment_id=1,
                content = "댓글1.1"
            )

            Comment.objects.create(
                id=6,
                user=User.objects.get(id=1),
                post=Post.objects.get(id=1),
                parent_comment_id=1,
                content = "댓글1.2"
            )

    def tearDown(self):
        Post.objects.all().delete()
        User.objects.all().delete()

    def test_comment_pagination_success(self):
        access_token = jwt.encode(
            {"id": self.test_user.id}, settings.SECRET_KEY, settings.ALGORITHM,
        )

        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}

        response = client.get("/posts/1/comments?parent_id=0&limit=2&offset=0", **header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "comments": [{
                "comment_id": 1,
                "user_id": 1,
                "email": "jiwon@mint.com",
                "content": "댓글1",
                "created_at": self.mocked_date_time.strftime('%Y-%m-%dT%H:%M:%S'),
                "updated_at": self.mocked_date_time.strftime('%Y-%m-%dT%H:%M:%S'),
                "parent_id": None

            },
            {
                "comment_id": 2,
                "user_id": 1,
                "email": "jiwon@mint.com",
                "content": "댓글2",
                "created_at": self.mocked_date_time.strftime('%Y-%m-%dT%H:%M:%S'),
                "updated_at": self.mocked_date_time.strftime('%Y-%m-%dT%H:%M:%S'),
                "parent_id": None
            }
        ]}
    )
    def test_user_error(self):
        access_token = jwt.encode(
            {"id": self.test_user.id}, settings.SECRET_KEY, settings.ALGORITHM,
        )[:-1]

        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}
        response = client.get("/posts/1/comments?parent_id=0&limit=2&offset=0", **header)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"MESSAGE": "INVALID_TOKEN"})

class PostTestCase(TestCase):
    maxDiff = None

    def setUp(self):
        self.client = Client()
        self.user_wanted = User.objects.create(
            email    = 'wanted@gmail.com',
            password = bcrypt.hashpw('12345678'.encode("utf-8"), bcrypt.gensalt()),
            name = '원티드',
        )

        self.user_wecode = User.objects.create(
            email    = 'wecode@gmail.com',
            password = bcrypt.hashpw('12345678'.encode("utf-8"), bcrypt.gensalt()),
            name = '위코드',
        )
        
        self.category_hobby = Category.objects.create(name='취미')
        self.category_python = Category.objects.create(name='파이썬')
        
        self.mocked_date_time = datetime.datetime(2021,1,1,0,0,0)

        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=self.mocked_date_time)):
            self.post_today_study =Post.objects.create(
                user        = self.user_wanted,
                subject     = '스터디 활동',
                content     = '오늘은 팀원들과 만나서 Python에 대해서 공부하였습니다.',
                category_id = self.category_python.id
            )

            self.post_today_hooby = Post.objects.create(
                user      = self.user_wanted,
                subject       = '오늘의 취미 활동',
                content     = '오늘은 등산을 하였습니다.',
                category_id = self.category_hobby.id
            )
    def tearDown(self):
        Post.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()

    def test_get_post_list(self):
        token = jwt.encode({"id": self.user_wanted.id }, settings.SECRET_KEY, settings.ALGORITHM)
        response = self.client.get('/posts', HTTP_Authorization=token)
        expected_data = {
            "results" : {
            "count" : 2,
            "data" : 
            [{
                "id": self.post_today_study.id,
                "user": self.user_wanted.name,
                "subject": "스터디 활동",
                "content": "오늘은 팀원들과 만나서 Python에 대해서 공부하였습니다.",
                "created_at": self.mocked_date_time.strftime('%Y-%m-%d %H:%M:%S'),
                "updated_at": self.mocked_date_time.strftime('%Y-%m-%d %H:%M:%S'),
                "view_count" : 0,
                "category_id" : self.category_python.id,
                "category" : self.category_python.name,

            },
            {
                "id": self.post_today_hooby.id,
                "user": self.user_wanted.name,
                "subject": "오늘의 취미 활동",
                "content": "오늘은 등산을 하였습니다.",
                "created_at": self.mocked_date_time.strftime('%Y-%m-%d %H:%M:%S'),
                "updated_at": self.mocked_date_time.strftime('%Y-%m-%d %H:%M:%S'),
                "view_count" : 0,
                "category_id" : self.category_hobby.id,
                "category" : self.category_hobby.name,


            }]
            }
        }
        self.assertEqual(response.json(), expected_data)
        self.assertEqual(response.status_code, 200)

    def test_get_post_list_using_pagination(self):
        token = jwt.encode({"id": self.user_wanted.id }, settings.SECRET_KEY, settings.ALGORITHM)
        response = self.client.get('/posts?offset=1&limit=1', HTTP_Authorization=token)
        expected_data = {
            "results" : {
            "count" : 2,
            "data" : 
            [{
                "id": self.post_today_hooby.id,
                "user": self.user_wanted.name,
                "subject": "오늘의 취미 활동",
                "content": "오늘은 등산을 하였습니다.",
                "created_at": self.mocked_date_time.strftime('%Y-%m-%d %H:%M:%S'),
                "updated_at": self.mocked_date_time.strftime('%Y-%m-%d %H:%M:%S'),
                "view_count" : 0,
                "category_id" : self.category_hobby.id,
                "category" : self.category_hobby.name,
            }]
            }
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_data)
    
    def test_get_post_list_using_pagination_and_search(self):
        token = jwt.encode({"id": self.user_wanted.id }, settings.SECRET_KEY, settings.ALGORITHM)
        response = self.client.get('/posts?offset=0&limit=1&subject=오늘의', HTTP_Authorization=token)
        expected_data = {
            "results" : {
            "count" : 1,
            "data" : 
            [{
                "id": self.post_today_hooby.id,
                "user": self.user_wanted.name,
                "subject": "오늘의 취미 활동",
                "content": "오늘은 등산을 하였습니다.",
                "created_at": self.mocked_date_time.strftime('%Y-%m-%d %H:%M:%S'),
                "updated_at": self.mocked_date_time.strftime('%Y-%m-%d %H:%M:%S'),
                "view_count" : 0,
                "category_id" : self.category_hobby.id,
                "category" : self.category_hobby.name,
            }]
            }
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_data)

    def test_create_blog_post_no_token(self):
        data = {
            'subject'     : '오늘의 영화',
            'content'   : '오늘의 영화는 코미디 입니다!',
            'category_id' : self.category_hobby.id,
        }
        response = self.client.post('/posts', data=data,  content_type='application/json')

        self.assertEqual(response.status_code, 401)

    def test_create_post(self):
        data = {
            'subject'     : '오늘의 영화',
            'content'     : '오늘의 영화는 코미디 입니다!',
            'category_id' : self.category_hobby.id,
        }
        
        token = jwt.encode({"id": self.user_wanted.id }, settings.SECRET_KEY, settings.ALGORITHM)
        response = self.client.post('/posts', data=data,  content_type='application/json', HTTP_Authorization=token)

        self.assertEqual(response.status_code, 201)

    def test_edit_post(self):
        data = {
            'subject'     : '오늘의 취미는?',
            'content'     : '오늘의 취미는 영화입니다!',
            'category_id' : self.category_hobby.id,
        }

        token = jwt.encode({"id": self.user_wanted.id }, settings.SECRET_KEY, settings.ALGORITHM)
        response = self.client.put(f'/posts/{self.post_today_hooby.id}', data=data,  content_type='application/json', HTTP_Authorization=token)

        self.assertEqual(response.status_code, 200)

    def test_edit_post_no_token(self):
        data = {
            'subject'     : '오늘의 취미는?',
            'content'     : '오늘의 취미는 영화입니다!',
            'category_id' : self.category_hobby.id,
        }
        response = self.client.put(f'/posts/{self.post_today_hooby.id}', data=data,  content_type='application/json')

        self.assertEqual(response.status_code, 401)

    def test_edit_post_diffent_user(self):
        data = {
            'subject'     : '오늘의 취미는?',
            'content'     : '오늘의 취미는 영화입니다!',
            'category_id' : self.category_hobby.id,
        }
        token = jwt.encode({"id": self.user_wecode.id }, settings.SECRET_KEY, settings.ALGORITHM)
        response = self.client.put(f'/posts/{self.post_today_hooby.id}', data=data, HTTP_Authorization=token,  content_type='application/json')

        self.assertEqual(response.status_code, 403)

    def test_delete_post(self):
        token = jwt.encode({"id": self.user_wanted.id }, settings.SECRET_KEY, settings.ALGORITHM)
        response = self.client.delete(f'/posts/{self.post_today_hooby.id}', HTTP_Authorization=token)

        self.assertEqual(response.status_code, 204)

    def test_delete_post_diffent_user(self):
        token = jwt.encode({"id": self.user_wecode.id }, settings.SECRET_KEY, settings.ALGORITHM)
        response = self.client.delete(f'/posts/{self.post_today_hooby.id}', HTTP_Authorization=token)

        self.assertEqual(response.status_code, 403)

    def test_delete_post_no_token(self):
        response = self.client.delete(f'/posts/{self.post_today_hooby.id}')

        self.assertEqual(response.status_code, 401)