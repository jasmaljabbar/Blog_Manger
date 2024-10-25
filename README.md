Blog Management System
This is a Blog Management System built using Django for the backend and React.js for the frontend. The system allows users to create, view, update, and delete blog posts. It supports authentication and authorization, and users can upload images for their blog posts.

Table of Contents
Project Overview
Features
Technologies Used
Installation
Usage
API Endpoints
Project Structure
Contributing
License
Project Overview
The Blog Management System is a full-stack web application designed to help users manage their blog posts. It provides functionality for user authentication, blog post creation, image upload, and real-time content management. This project demonstrates the integration of Django for the backend API and React.js for the frontend UI.

Features
User Authentication: Secure user registration, login, and logout.
Create, Update, and Delete Blog Posts: Users can manage their own blog content.
Image Upload: Blog posts can include image attachments with file validation.
Responsive Design: The frontend is fully responsive, built with Tailwind CSS.
Slug-Based URL Routing: Uses slugs for human-readable URLs.
Error Handling: Custom error handling, including validation for duplicate titles.
Role-Based Permissions: Only authors can edit or delete their own posts.
Technologies Used
Backend: Django, Django REST Framework, SQLite
Frontend: React.js, Tailwind CSS
State Management: React Hooks, Formik for form management
API: RESTful API with Django
Other Tools: Axios, Yup for validation
Installation
Prerequisites
Ensure that you have the following installed:

Python 3.x
Node.js & npm
Django 4.x
SQLite (or another database if preferred)
