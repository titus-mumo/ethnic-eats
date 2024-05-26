# from .models import CommunityForumModel
# from django.http import JsonResponse
# from rest_framework import status, permissions
# from rest_framework.views import APIView
# from django.contrib.auth.models import User
# from .serializers import GetForumSerializer


# class CommunityForum(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     #Join a commnunity forum
#     def post(self, request, communityforum_id):
#         user = request.user
#         try:
#             community_forum = CommunityForumModel.objects.filter(communityforum_id = communityforum_id).first()
#         except CommunityForumModel.DoesNotExist():
#             return JsonResponse({"error": "Community Forum not found"}, status = status.HTTP_404_NOT_FOUND)
        
#         if community_forum.members.filter(user = user).exists():
#             return JsonResponse({"message": "You are already a member of this community forum."}, status=status.HTTP_200_OK)
        
#         else:
#             community_forum.members.add(user)
#             return JsonResponse({"message": "You have successfully joined the community forum."}, status=status.HTTP_201_CREATED)
        
# class AllCommunityForums(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         queryset = CommunityForumModel.objects.all()
#         serialized_forums = GetForumSerializer(queryset, many=True)
#         return JsonResponse(serialized_forums.data, status = status.HTTP_200_OK, safe=False)
        


        


