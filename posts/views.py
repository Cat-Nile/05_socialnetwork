from operator import ge
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Post
from .permissions import CustomReadOnly
from .serializers import PostSerializer, PostCreateSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [CustomReadOnly]
    filter_backends = [SearchFilter, OrderingFilter,]
    search_fields = ['title']
    ordering_fields = ['created_at', 'hits', 'likes']
    ordering = ['created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PostSerializer
        elif self.action == 'retrieve':
            inst=self.get_object()
            inst.hits += 1
            inst.save()
            return PostSerializer
        return PostCreateSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    
    return Response({'status': 'ok'})
