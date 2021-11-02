import json, re, bcrypt, jwt 
from json              import JSONDecodeError

from django.views      import View
from django.http       import JsonResponse
from django.shortcuts  import get_object_or_404
from django.db.models  import F

from posts.models      import Post, Comment, Category
from users.models      import User, AccessLog
from users.decorators  import login_decorator


class CommentView(View):
    @login_decorator
    def get(self, request, post_id):
        comments = Comment.objects.filter(post_id=post_id).select_related('user').order_by('-id')

        comment_list = [{   
                'user_id'    : comment.user_id,
                'email'      : comment.user.email,
                'content'    : comment.content,
                'created_at' : comment.created_at,
                'parent_id'  : comment.parent_comment_id,
                } for comment in comments
            ]
        return JsonResponse({'comments':comment_list}, status=200)

    @login_decorator
    def post(self, request, post_id):
        try:
            data = json.loads(request.body)
            user = request.user

            if not Post.objects.filter(id=post_id).exists():
                return JsonResponse({'message':'POST_DOES_NOT_EXIST'}, status=404)

            Comment.objects.create(
                content           = data.get('content', None),
                user              = user,
                post_id           = post_id,
                parent_comment_id = data.get('parent_comment_id', None)
            )

            return JsonResponse({'message':'SUCCESS'}, status=201)
        
        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
    
    @login_decorator
    def patch(self, request, post_id):
        try:
            data        = json.loads(request.body)

            if Comment.objects.filter(post_id=post_id, user_id=request.user.id):
                Comment.objects.update(
                    user        = request.user,
                    post_id     = post_id,
                    content     = data['content']
                )
                return JsonResponse({'MESSAGE' : 'COMMENT_UPDATED'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

    @login_decorator
    def delete(self, request, post_id):
        comment = Comment.objects.filter(post_id=post_id, user_id=request.user.id)
        if not comment.exists():
            return JsonResponse({'MESSAGE' : 'COMMENT_DOES_NOT_EXIST'}, status=400)

        comment.delete()
        return JsonResponse({'MESSAGE' : 'COMMENT_DELETED'}, status=204)


class PostListCreateView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = request.user.id
            
            if data['subject'] == '':
                return JsonResponse({'MESSAGE': 'SUBJECT_ERROR'}, status=400)
            
            if data['content'] == '':
                return JsonResponse({'MESSAGE': 'CONTENT_ERROR'}, status=400)

            category_id = int(data['category'], -1)
            if not Category.objects.filter(category_id=category_id).exists():
                return JsonResponse({'MESSAGE': 'CATEGORY_ERROR'}, status=400)

            Post.objects.create(
                    user     = User.objects.get(id=user_id),
                    subject  = data['subject'],
                    content  = data['content'],
                    category_id = category_id
                )

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

    @login_decorator
    def get(self, request):
        limit  = int(request.GET.get('limit','20'))
        offset = int(request.GET.get('offset','0'))
        offset = offset * limit

        post_count = Post.objects.all().count()
        posts = Post.objects.all()[offset:offset+limit]
        
        posts_list = [{
            'user'   : post.user.name,
            'subject' : post.subject,
            'content' : post.content,
            'category' : post.category.name,
            'view_count' : post.viewcount,
            'created_at' : post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at' : post.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        } for post in posts]

        result = {
            'count': len(post_count),
            'data' : posts_list
        }
        return JsonResponse({'results': result}, status=200)

class PostRetrieveDeleteEditView(View):
    @login_decorator
    def get(self, request, post_id):
        try:
            user_id = request.user.id
            post = get_object_or_404(Post, id=post_id)
            _, is_exsist = AccessLog.objects.get_or_create(post_id=post_id, user_id=user_id)

            if not is_exsist:
                post.viewcount = F('viewcount') + 1
                post.save()
            
            post_data = {
                'user'   : post.user.name,
                'subject' : post.subject,
                'content' : post.content,
                'category' : post.category.name,
                'view_count' : post.viewcount,
                'created_at' : post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at' : post.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            }

            result = {
                'data' : post_data
            }

            return JsonResponse({'results': result}, status=200)
    
        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE': 'POST_DOSE_NOT_EXIST'}, status=404)

    @login_decorator
    def put(self, request, post_id):
        try:
            data = json.loads(request.body)
            post = get_object_or_404(Post, id=post_id)
            
            if data['subject'] == '':
                return JsonResponse({'MESSAGE': 'SUBJECT_ERROR'}, status=400)
            
            if data['content'] == '':
                return JsonResponse({'MESSAGE': 'CONTENT_ERROR'}, status=400)

            category_id = int(data['category'], -1)
            if not Category.objects.filter(category_id=category_id).exists():
                return JsonResponse({'MESSAGE': 'CATEGORY_ERROR'}, status=400)

            post.subject = data['subject']
            post.content = data['content']
            post.category_id = category_id
            post.save()

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE': 'POST_DOSE_NOT_EXIST'}, status=404)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

    @login_decorator
    def delete(self, request, post_id):
        try:
            post = get_object_or_404(Post, id=post_id)

            if not request.user.id == post.user.id:
                    return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=403)
            
            post.delete()
            return JsonResponse({'MESSAGE': 'NO_CONTENT'}, status=204)

        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE': 'POST_DOSE_NOT_EXIST'}, status=404)