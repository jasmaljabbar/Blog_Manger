from django.utils.text import slugify
from rest_framework import serializers
from .models import Blog

class BlogSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'image', 'author', 
                 'author_name', 'created_at', 'updated_at', 
                 'slug', 'is_author']
        read_only_fields = ['author', 'slug']

    def get_is_author(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.author == request.user
        return False
    
    def validate_title(self, value):
        """
        Custom validation to check for the uniqueness of the slug generated from the title.
        """
        slug = slugify(value)  # Create slug from the title
        if Blog.objects.filter(slug=slug).exists():
            raise serializers.ValidationError("A blog with this title already exists. Please use a different title.")
        return value

    def validate_image(self, value):
        if value:
            # Max file size of 5MB
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("Image size cannot exceed 5MB")
            # Validate file type
            if not value.content_type.startswith('image/'):
                raise serializers.ValidationError("Only image files are allowed")
        return value