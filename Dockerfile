# Use Python 3.9.6 as the base image
FROM python:3.9.6

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG True

# Set the working directory in the container
WORKDIR /code

# Install system dependencies
RUN apt-get update \
    && apt-get install -y libpq-dev

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all the files to the container
COPY . /code/

# Expose the port on which the Django app will run
EXPOSE 8000

# Run the Django development server
CMD python manage.py runserver 0.0.0.0:8000
