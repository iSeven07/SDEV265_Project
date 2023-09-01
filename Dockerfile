# Use the official lightweight Python image
FROM python:3.8-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED True

EXPOSE 8000

# Copy local code to the container image
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies
RUN pip install -r requirements.txt

# Run the web service on container startup
WORKDIR /app/src
CMD python manage.py runserver