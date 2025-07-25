from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, permissions, generics, filters
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Note
from .serializers import NoteSerializer, UserRegisterSerializer, UserLoginSerializer


@api_view(['GET'])
def health(request):
    """Simple health check endpoint"""
    return Response({"message": "Server is up!"})

# PUBLIC_INTERFACE
class RegisterView(APIView):
    """
    Register a new user.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PUBLIC_INTERFACE
class LoginView(APIView):
    """
    User login endpoint.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data["username"], password=serializer.validated_data["password"])
            if user:
                login(request, user)
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PUBLIC_INTERFACE
class LogoutView(APIView):
    """
    User logout endpoint.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

# PUBLIC_INTERFACE
class NoteListCreateView(generics.ListCreateAPIView):
    """
    List and create notes (owned by the authenticated user).
    Supports search by title/content.
    """
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# PUBLIC_INTERFACE
class NoteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a note. Only owner can access.
    """
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "note_id"

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)
