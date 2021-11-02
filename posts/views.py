import json, re, bcrypt, jwt 

from django.views            import View
from django.http             import JsonResponse

from posts.models            import Post, Comment
from users.models            import User
from users.utils             import login_decorator

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

            if not (content and post_id):
                return JsonResponse({'message':'KEY_ERROR'}, status=400)

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