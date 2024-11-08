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
            # Expecting the image URL to be passed in request.data, not in request.FILES
            image_url = self.request.data.get('image')  # Get the image URL directly from the request data
            if image_url:
                serializer.save(author=self.request.user, image=image_url)  # Save blog with the image URL
            else:
                serializer.save(author=self.request.user)
        except IntegrityError as e:
            # Catch duplicate slug error and raise a ValidationError
            if 'UNIQUE constraint failed' in str(e):
                raise ValidationError({'detail': 'A blog with this title already exists. Please choose a different title.'})
            raise e



   

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        
        updated_data = request.data.copy()  # This should be fine if it's a MultiValueDict
        updated_data = {key: value[0] for key, value in updated_data.lists()}  # Convert QueryDict to dict

        # Handle image update
        if 'image' in updated_data and updated_data['image']:
            image_url = updated_data['image']
            updated_data['image'] = image_url
        else:
            # If image field is empty, keep existing image
            if 'image' in updated_data:
                updated_data.pop('image')
        serializer = self.get_serializer(instance, data=updated_data, partial=partial)

        # Validate the serializer
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            print("Serializer Errors:", e.detail)  # Log the errors
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        # Save changes
        self.perform_update(serializer)
        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            
            # Optionally, log or handle the URL before deleting
            image_url = instance.image
            if image_url:
                # Here you could add logic to delete the image from the storage service
                # For example, if using a service like Cloudinary or AWS S3, delete the image
                # cloudinary.uploader.destroy(image_url)  # This is just an example

                # If you're just using URLs and don't need to delete anything:
                print(f"Image at {image_url} would be deleted from cloud storage.")  # Placeholder
                
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)


