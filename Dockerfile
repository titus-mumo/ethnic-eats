# Use the official Python image from the Docker Hub
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Download NLTK data
RUN python -m nltk.downloader vader_lexicon

# Copy the Django project
COPY . /code/

# Expose the port the app runs on
EXPOSE 8000

# Run the Django development server
CMD ["python", "ethnic_eats/manage.py", "runserver", "0.0.0.0:8000"]
