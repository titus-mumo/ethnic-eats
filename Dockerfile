# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /ethnic_eats

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -m nltk.downloader vader_lexicon

# Copy the current directory contents into the container at /app
COPY . /ethnic_eats/

# Make port 8000 available to the world outside this container
EXPOSE 10000

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=ethnic_eats.settings
ENV PYTHONUNBUFFERED=1

# Run database migrations and collect static files
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Define the command to run the application using Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "ethnic_eats.asgi:application"]


