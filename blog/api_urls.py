from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import *
from bookstore.urls import router

router.register(r'blog/category', BlogCategoryViewSet,basename='category')
router.register(r'blog/blogs', BlogViewSet,basename='blogs')
router.register(r'blog/comments', CommentViewSet,basename='comments')


urlpatterns = [
    path('', include(router.urls)),
]