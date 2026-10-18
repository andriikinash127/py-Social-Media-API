from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Post
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.select_related("author").all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.select_related("author").all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
