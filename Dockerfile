FROM python:3.9-buster
ENV PYTHONUNBUFFERED=1

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install "gunicorn==20.1.0"
COPY . /code/

# # Collect static files
# #RUN python manage.py collectstatic --noinput

# # Run Gunicorn
# #CMD ["gunicorn", "--workers=3", "-b", "0.0.0.0:8000", "--timeout", "120", "--log-level", "debug", "masterrisk.wsgi"]

# Use an official Python runtime as a parent image
# FROM python:3.8

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Set the working directory in the container
# WORKDIR /app

# # Install system dependencies
# RUN apt-get update && \
#     apt-get install -y libpq-dev

# # Install Python dependencies
# COPY requirements.txt /app/
# RUN pip install --upgrade pip && \
#     pip install -r requirements.txt

# # Copy the current directory contents into the container
# COPY . /app/

# # Apply database migrations
# RUN python manage.py migrate

# # Collect static files
# RUN python manage.py collectstatic --noinput

# # Create the admin user (replace these values with your own)
# RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')" | python manage.py shell

# # Expose port 8000 for the Django development server
# EXPOSE 8000

# # Start the Django development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
