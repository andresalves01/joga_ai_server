# Use the official Python image for Python 3.10 based on Alpine Linux
FROM python:3.10-alpine

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Set the working directory in the container
WORKDIR /app

# Install system dependencies and clean up
RUN apk --no-cache add libffi-dev gcc musl-dev \
  && pip install --no-cache-dir --upgrade pip \
  && apk del libffi-dev gcc musl-dev

# Copy the entire application directory into the container
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app runs on
EXPOSE 5000

# Change the working directory to /app/src
WORKDIR /app/src

# Start your Flask application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
