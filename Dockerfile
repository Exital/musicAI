# Use Python Alpine as the base image
FROM python:3.10-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG True

# Set the working directory in the container
WORKDIR /code

# Install dependencies
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev

# Copy requirements.txt to the container
COPY requirements.txt /code/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all the files to the container
COPY . /code/

# Expose the port on which the Django app will run
EXPOSE 8000

# Run the Django development server
CMD python manage.py runserver 0.0.0.0:8000
