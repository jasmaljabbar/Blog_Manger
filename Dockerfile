# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file first for efficient caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Set the environment variable for Django settings module (optional)
ENV DJANGO_SETTINGS_MODULE=blogmanagement.settings

# Collect static files (only if your project requires it for production)
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on (Django default is 8000)
EXPOSE 8000

# Start the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "blogmanagement.wsgi:application"]
