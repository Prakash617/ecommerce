from django.urls import path
from . import views

urlpatterns = [
    path('feedback/', views.feedback_view, name='feedback'),
    path('feedback/success/<int:pk>/', views.feedback_success_view, name='feedback_success'),
    path('feedback/registrations/', views.feedback_list_view, name='feedback_list'),


]