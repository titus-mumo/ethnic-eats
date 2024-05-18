from rest_framework.views import APIView
from .serializers import UserPostGetSerializer, UserPostPostSerielizer
from .models import UserPost
from django.http import JsonResponse
from rest_framework import status, permissions





# user post
class UserPostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        post_description = request.data.get('post_description')
        post = {}
        post['user'] = user.id
        post['post_description'] = post_description
        post_serializer = UserPostPostSerielizer(data = post)
        if post_serializer.is_valid():
            print("Data is serialized")
            post = UserPost.objects.create(
                post_description=post['post_description'], post_owner=user)
            serializer = UserPostGetSerializer(post, many=False)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        
    def get(self, requet):
        posts = UserPost.objects.all()
        serializer = UserPostGetSerializer(posts, many = True)
        return JsonResponse(serializer.data, status = status.HTTP_200_OK, safe=False)
