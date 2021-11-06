# Use an official Python runtime as a parent image
FROM python:latest

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Adding backend directory to make absolute filepaths consistent across services
WORKDIR /app/backend

# Install Python dependencies
COPY ./requirements /app/backend/requirements
RUN pip install -r requirements/development.txt

COPY ./entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# Add the rest of the code
COPY . /app/backend

# Make port 8000 available for the app
EXPOSE 8000

# Be sure to use 0.0.0.0 for the host within the Docker container,
# otherwise the browser won't be able to find it
ENTRYPOINT ["/entrypoint"]
