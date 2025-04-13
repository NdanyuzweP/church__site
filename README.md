# Bash script to create the Django project directory structure

mkdir -p Church_site/{church_project,church_app/migrations,templates/church_app,static/{css,js,images},media}

# Create essential Python files
touch Church_site/README.md
touch Church_site/manage.py
touch Church_site/requirements.txt

# Django project files
touch Church_site/church_project/__init__.py
touch Church_site/church_project/settings.py
touch Church_site/church_project/urls.py
touch Church_site/church_project/asgi.py
touch Church_site/church_project/wsgi.py

# Django app files
touch Church_site/church_app/__init__.py
touch Church_site/church_app/admin.py
touch Church_site/church_app/apps.py
touch Church_site/church_app/forms.py
touch Church_site/church_app/models.py
touch Church_site/church_app/urls.py
touch Church_site/church_app/views.py

# Sample templates
touch Church_site/templates/church_app/index.html
touch Church_site/templates/church_app/contact.html

echo "✅ Church_site directory structure created successfully!"
