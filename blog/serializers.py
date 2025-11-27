from rest_framework import serializers
from .models import Blog, BlogCategory,Comment

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    comment_on = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id','replies', 'name', 'email', 'user', 'parent_comment', 'comment', 'post', 'comment_on', 'is_spam']

    def get_comment_on(self, obj):
        return obj.comment_on.strftime('%d %B %Y')

    def get_replies(self, obj):
        # Serializer method to include replies
        replies = Comment.objects.filter(parent_comment=obj)
        serializer = CommentSerializer(replies, many=True)
        return serializer.data

