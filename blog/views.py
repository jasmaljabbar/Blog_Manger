from django.db import IntegrityError
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Blog
from .serializers import BlogSerializer
from rest_framework.exceptions import ValidationError

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    # Change lookup_field to 'id' to use IDs for lookups
    lookup_field = 'id'  # Use ID instead of slug
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user)
        except IntegrityError as e:
            # Catch duplicate slug error and raise a ValidationError
            if 'UNIQUE constraint failed' in str(e):
                raise ValidationError({'detail': 'A blog with this title already exists. Please choose a different title.'})
            raise e

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Handle image update
        if 'image' in request.FILES:
            # Delete old image if it exists
            if instance.image:
                instance.image.delete(save=False)
        elif 'image' in request.data and not request.data['image']:
            # If image field is empty in request, keep existing image
            request.data.pop('image')

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Delete associated image if it exists
        if instance.image:
            instance.image.delete()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
