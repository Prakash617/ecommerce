from rest_framework import viewsets, serializers
from .models import Blog, BlogCategory
from .serializers import *
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import permissions

class BlogCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes =[AllowAny]

class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'slug'
    permission_classes =[AllowAny]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(is_spam=False,parent_comment=None)
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    permission_classes = ('post','get')

    def perform_create(self, serializer):
        user=self.request.user
        # Automatically set the user field to the logged-in user
        serializer.save(user=user,name=user.full_name,email=user.email)

    def get_queryset(self):
        queryset = super().get_queryset()
        # Optionally filter comments based on the request, for example, only return comments for a specific blog post
        
        try:
            post_id = self.request.query_params.get('post_id')
            post = Blog.objects.get(id=post_id)
            queryset = queryset.filter(post=post)
        except:
            return Comment.objects.none()
        return queryset
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAuthenticated()]


    
