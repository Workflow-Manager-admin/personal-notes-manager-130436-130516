from django.urls import path
from .views import (
    health,
    RegisterView,
    LoginView,
    LogoutView,
    NoteListCreateView,
    NoteRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('health/', health, name='Health'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('notes/', NoteListCreateView.as_view(), name='note-list-create'),
    path('notes/<int:note_id>/', NoteRetrieveUpdateDestroyView.as_view(), name='note-detail'),
]
