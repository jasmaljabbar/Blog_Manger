from django.utils.text import slugify
from rest_framework import serializers
from .models import Blog

class BlogSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    is_author = serializers.SerializerMethodField()
    image = serializers.CharField(required=False, allow_blank=True)

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
        slug = slugify(value)  # Create slug from the title
        
        # Check for existing slugs, considering the instance
        if self.instance:
            # Exclude current instance if it exists (for updates)
            if Blog.objects.filter(slug=slug).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError(f"A blog with the slug '{slug}' already exists. Please use a different title.")
        else:
            # For new instance creation
            if Blog.objects.filter(slug=slug).exists():
                raise serializers.ValidationError(f"A blog with the slug '{slug}' already exists. Please use a different title.")

        return value
